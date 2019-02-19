using System;
using System.Diagnostics;
using System.Net.NetworkInformation;
using System.Threading.Tasks;

namespace iolog
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Give an address");
                return;
            }
            
            var addr = args[0];
            
            var tOut = args.Length > 1 ? int.Parse(args[1]) : 100; // ms
            var tEnd = args.Length > 2 ? int.Parse(args[2])*60 : 60; // sec

            var tStart = DateTime.Now;
            var dt  = 0;
            var nOut = 0;
            var nSent = 0;
            var rttTotal = 0.0;
            var rttMin = 1e6;
            var rttMax = 0.0;

            var ping = new Ping();
            do 
            {
                await Task.Run(async () =>
                {
                    var sw = new Stopwatch();
                    sw.Start();
                    await new Ping().SendPingAsync(addr, 100000);
                    sw.Stop();
                    var rtt = sw.Elapsed.Milliseconds;
                    dt = (int) DateTime.Now.Subtract(tStart).TotalSeconds;
                    
                    if (rtt < rttMin)
                        rttMin = rtt;
                    
                    if (rtt > rttMax)
                        rttMax = rtt;

                    if (rtt > tOut) {
                        nOut++;
                        Console.WriteLine($"{dt}: {rtt} ms");
                    }
                    
                    nSent++;
                    rttTotal += rtt;
                });
            }  while (dt < tEnd);

            Console.WriteLine($"Outage threshold {tOut} msecs");
            var mean = Math.Ceiling(rttTotal/nSent);
            Console.WriteLine($"Sent {nSent} packets, {nOut} in outage, average rtt {mean}, min {rttMin}, max {rttMax} msecs");
        }
    }
}
