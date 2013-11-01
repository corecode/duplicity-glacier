#!/usr/bin/env ruby

require 'optparse'

dryrun = []

op = OptionParser.new do |opts|
  opts.banner = "usage: s3-rename.rb [-n] s3://PATH"

  opts.on("--dryrun", "-n", "Do a dryrun") do |v|
    dryrun = %w{-n}
  end
end
op.parse!

s3dir = ARGV[0]

if !s3dir
  $stderr.puts op
  exit 1
end

IO.popen(%w{s3cmd ls} + [s3dir]) do |io|
  io.each do |l|
    _, _, _, fn = l.chomp.split(/\s+/, 4)

    if /(.*\/)(duplicity.*vol.*difftar.*)/.match(fn)
      p = Process.fork do
        exec *(%w{s3cmd mv} + dryrun + [fn, $1+"data-"+$2])
      end
    end
  end
end

while true
  begin
    Process.wait
  rescue Errno::ECHILD
    break
  end
end
