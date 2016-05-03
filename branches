#! /usr/bin/ruby

cd = Dir.pwd

dir = ARGV[0] ? "#{ENV['HOME']}/w/#{ARGV[0]}" : ENV['PWD']

Dir.entries(dir)[2..-1].each do |d|
  f = File.join(dir,d)
  next unless File.directory? f
  Dir.chdir f
  %x(git branch).split(/\n/).each {|b| puts "#{d}: #{b[2..-1]}" if b.include? '*'}
end

Dir.chdir cd
