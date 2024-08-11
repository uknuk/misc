#! /usr/bin/env ruby

# ping statistics - histogram of delay distribution

Bin = [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 3, 5, 100]

def add(d, v)
  i = Bin.index {|n| n > v}
  i = bin.size unless i
  d[i-1] += v
end

def count(d)
  s = d.reduce(:+)
  d.map {|n| '%.2f' % [n/s*100]}
end


ip = ARGV[0]
unless ip
  puts "Give an ip address or host to ping"
  exit
end

Tend =  ARGV.size > 1 ? ARGV[1].to_i : 60 #min
Tshow = ARGV.size > 2 ? ARGV[2].to_i : 60 #sec

tStart = Time.now
tEnd = tStart + Tend*60
tShow = tStart + Tshow

d = []
Bin.size.times { d << 0 }
out = false

tNow = Time.now
tOut = 0

while tNow < tEnd
  res = %x(ping -c 1 -W 1 #{ip} 2>&1).split(/\n/)[-1] # timeout 1 sec
  begin
    v = res.split('=')[1].split('/')[0].to_f/1000
    if out
      out = false
      add(d, tOut)
      tOut = 0
    end
    add(d, v)
  rescue
    out = true unless out
    tOut += 1
  end

  if tNow > tShow
    tShow += Tshow
    puts "Elapsed #{(tNow - tStart).to_i} sec"
    puts "sec\t" + Bin.join("\t")
    puts "%\t" + count(d).join("\t")
  end
  tNow = Time.now
end
    
      
    
