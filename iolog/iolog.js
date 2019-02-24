#! /usr/bin/env node
// sudo -s ./iolog.js

const {promisify} = require('util'),
    sleep = promisify(setTimeout),
    lookup = promisify(require('dns').lookup),
    moment = require('moment')
    ping = require('net-ping'),
    program = require('commander');

program
    .option('-t --time [val]', 'run time in seconds, default 60', 60)
    .option('-i --interval [val]', 'interval between pings in msecs, default 10', 10)
    .option('-o --outage [val]', 'outage threshold in msecs')
    .parse(process.argv)



async function main(host, args) {
    const ip = (await lookup(host)).address;
    console.log(`Pinging to ${ip} for ${args.time} seconds with interval of ${args.interval} msecs`)
    if (args.outage)
        console.log(`outage threshold ${args.outage} msecs`)
    const session = ping.createSession();
    const start = moment();
    let stat = {
        sent: 0,
        recv: 0,
        out: 0,
        mean: 0.0,
        min: 1e6,
        max: 0
    }
    let now;

    do {
        session.pingHost(ip, (err, target, sent, recv) => {
            if (err)
                console.log(err);
            else {
                stat.recv++;
                let rtt = recv - sent;
                if (!rtt)
                    rtt = 1;
                stat.mean += rtt;
                if (rtt > stat.max)
                    stat.max = rtt;
                if (rtt < stat.min)
                    stat.min = rtt;
                if (args.outage && rtt > args.outage) {
                    stat.out++;
                    console.log(`outage ${rtt}`)
                }
            }
        });
        await sleep(args.interval);
        stat.sent++;
        now = moment();
    } while(now.diff(start, 'seconds') < args.time)
    
    await sleep(1000);
    return Promise.resolve(stat);
}

if (process.argv.length == 2) {
    console.log("Give an address");
    process.exit(1);
}

const host = program.args[0];

main(host, program)
    .then(stat => {
        stat.mean /= stat.recv;
        console.log(`Sent ${stat.sent}, replied ${stat.recv}`);
        console.log(`mean ${stat.mean.toFixed(2)}, max ${stat.max}, min ${stat.min} msecs`);
        if (program.outage)
            console.log(`${stat.out} packets over outage thershold ${program.outage} msecs`)
    });