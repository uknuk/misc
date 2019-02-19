#! /usr/bin/env ruby

# icmp outage log

require './icmp'
require 'thread'

SEQMAX = 65536 # icmp sequence

Tstep = ARGV.size > 3 ? ARGV[3].to_f/1000 : 0.005
Tend = ARGV.size > 2 ? ARGV[2].to_f*60 : 3600
Tout = ARGV.size > 1 ? ARGV[1].to_f/1000 : 0.2  

ip = ARGV[0]

Nth = Tend/Tstep # number of echoes

Tdel = Tstep + 0.01

mutex = Mutex.new


ts = Array.new(Nth) # time of sending 
tr = Array.new(Nth) # time of reception

send = ICMP.send(ip)

id = 0
t0 = Time.now

run = true

puts 'Starting at ' + t0.strftime('%H:%M:%S') 

Thread.new do
  ns = 0
  while ns < Nth
    unless send.call(ns/SEQMAX, ns%SEQMAX)
      $stderr.puts "sending echo fail"
      exit
    end
    mutex.synchronize { ts[ns] = Time.now }
    ns += 1
    sleep Tstep
  end
end


Thread.new do
  s = ICMP.make_sock
  while run
    n1, n2 = ICMP.recv(s)
    if n1 and n2
      nr = n1*SEQMAX + n2
      mutex.synchronize  { tr[nr] = Time.now }
    end
  end
end



nOut = 1
out = false
p = 0  # outage packet counter
tStart = 0 # start of outage
k = 0
tsk = trk = nil

sleep 10*Tout

while k < Nth 
    sleep Tdel
    mutex.synchronize { tsk,trk  = [ts[k], tr[k]] }
    
    next unless tsk
      
    out = trk ? trk - tsk > Tout : true
 
    if out
      tStart = tsk if p == 0
      p += 1
    elsif p > 0
      pn = p > 1 ? "#{k-p} - #{k-1}" : k-1
      tout = ((tsk - tStart)*1000).to_i
      # measured on sending side because it's monotonic
      dt = '%.3f' % (tsk - t0) # strftime doesn't show ms
      puts "#{nOut}, #{tsk.strftime('%H:%M:%S')}, #{dt}, #{tout} ms, #{p}, #{pn}" 
      nOut += 1
      p = 0
    end
    k  += 1
end

puts 'Finished at ' + Time.now.strftime('%H:%M:%S')

run = false





