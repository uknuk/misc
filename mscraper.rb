#!/usr/bin/env ruby

require 'mechanize'

m = Mechanize.new
name = ARGV[0]
range = ARGV[1]

base = File.read(File.join(ENV['HOME'], '.mscraper')).chop
url = "#{base}/#{name}.html"

links = []
fnames = []
num = 0

m.get(url).links_with(href: %r{/download/}).each do |link|
   unless link.href.include? '/play/'
    num += 1
    snum = num < 10 ? "0#{num}" : num
    fnames << "#{snum}-#{link.href.split('/')[2]}.mp3"
    links << link
   end
end

fnames = fnames[0..-10]
if range
  eval("fnames = fnames[#{range}]")
end

size = fnames.size
puts "Downloading #{size} files:"
fnames.map! {|f| f.sub("#{name}_",'')}
fnames.each {|f| puts f}
fnames.each_with_index do |fn, n|
    puts "Downloading #{fn}"
    puts
    flink = links[n].click.forms[1].submit.link_with(href: %r{/download/}).href
    %x(wget -O #{fn} #{flink})
end
