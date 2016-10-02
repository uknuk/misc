#!/usr/bin/env ruby

require 'mechanize'

m = Mechanize.new
name = ARGV[0]

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


last = ARGV[1] ? ARGV[1].to_i : fnames.size - 10
puts "Downloading #{last} files:"
fnames = fnames[0..last-1].map {|f| f.sub("#{name}_",'')}
fnames.each {|f| puts f}
last.to_i.times.each do |n|
    puts "Downloading #{fnames[n]}"
    puts
    flink = links[n].click.forms[1].submit.link_with(href: %r{/download/}).href
    %x(wget -O #{fnames[n]} #{flink})
end
