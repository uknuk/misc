
open System
open System.Net.NetworkInformation

let argv = fsi.CommandLineArgs
let host = argv.[1]
let argc = fsi.CommandLineArgs.Length
let tEnd = if argc > 2 then int(argv.[2]) else 60
let tOut = if argc > 3 then int(argv.[3]) else 100

let tStart = DateTime.Now

type Stat = {
    mutable total: int; 
    mutable min: int; 
    mutable max: int; 
    mutable recv: int;
    mutable out: int
}

let update (stat: Stat) (rttL: int64) =
    let rtt = int rttL
    if rtt < stat.min then stat.min <- rtt
    if rtt > stat.max then stat.max <- rtt
    if rtt > tOut then
        printfn "outage %d" rtt
        stat.out <- stat.out + 1

    stat.total <- stat.total + rtt
    stat.recv <- stat.recv + 1

let stat = {total = 0; min = 1000; max = 0; recv = 0; out = 0}

let ping = async {
    let! reply = (new Ping()).SendPingAsync(host) |> Async.AwaitTask |> Async.Catch
    match reply with
    | Choice1Of2 data -> update stat data.RoundtripTime // int(data) error?
    | Choice2Of2 e -> printfn "%s" e.Message
}

let mutable sent = 0
while int(DateTime.Now.Subtract(tStart).TotalSeconds) < tEnd do
    Async.RunSynchronously ping
    sent <- sent + 1

let mean = double(stat.total)/double(stat.recv) |> Math.Ceiling |> int
printfn "Sent %d, replied %d" sent stat.recv
printfn "mean %d, min %d, max %d" mean stat.min stat.max
if stat.out > 0 then
    printfn "%d packets over outage theshold %d" stat.out tOut


