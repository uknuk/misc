require 'socket'
require 'timeout'


module ICMP

  REPLY = 0
  ECHO  = 8
  SUB  =  0

  FORMAT = 'C2 n3 A'
  DEFPKTSIZE = 56
  TIMEOUT = 1

 
  def self.make_data(size)
    data = ''
    0.upto(size){ |n| data << (n % 256).chr }
    data
  end

  
   # Perform a checksum on the message.  This is the sum of all the short
    # words and it folds the high order bits into the low order bits.
    #
    def self.checksum(msg)
      length    = msg.length
      num_short = length / 2
      check     = 0

      msg.unpack("n#{num_short}").each do |short|
        check += short
      end

      if length % 2 > 0
        check += msg[length-1, 1].unpack('C').first << 8
      end

      check = (check >> 16) + (check & 0xffff)
      return (~((check >> 16) + check) & 0xffff)
    end

    def self.make_pkt(id, seq, data, format)
      pkt = [ECHO, SUB, 0, id, seq, data]
      pkt[2] = checksum(pkt.pack(format))
      pkt.pack(format)
    end


    def self.make_sock(host = nil) # local host address
      sock = Socket.new(Socket::PF_INET, Socket::SOCK_RAW, Socket::IPPROTO_ICMP)
      if host
         saddr = Socket.pack_sockaddr_in(0, host)
         sock.bind(saddr)
      end
      sock
    end

    def self.send(rhost, size = DEFPKTSIZE, lhost=nil)
      sock = make_sock(lhost)
      format = FORMAT << size.to_s
      data = make_data(size)
      # id = Process.pid & 0xffff unless id
      
      lambda do |id, seq|
          pkt = make_pkt(id, seq, data, format)
          begin
            saddr = Socket.pack_sockaddr_in(0, rhost)
          rescue Exception
            sock.close unless soc.closed?
            return false
          end
          sock.send(pkt, 0, saddr)
          return true
      end
    end
    
    def self.recv(sock)
      id = seq = nil
      io_array = select([sock], nil, nil, TIMEOUT)
      
      if io_array.nil? || io_array[0].empty?
           return nil
      end

      data = sock.recvfrom(1500).first
      if data[20, 2].unpack('C2').first == REPLY
         id, seq = data[24, 4].unpack('n3')   
      end
      return [id, seq]        
    end

end
      
  


