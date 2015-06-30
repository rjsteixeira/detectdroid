#!/usr/bin/python
from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
from pydhcplib.dhcp_constants import *


netopt = {
    'client_listen_port':"68",
    'server_listen_port':"67",
    'listen_address':"0.0.0.0"
}

class Server(DhcpServer):
    def __init__(self, options):
        DhcpServer.__init__(
            self,options["listen_address"],
            options["client_listen_port"],
            options["server_listen_port"])

    def PrintOptions(self, packet, options=['vendor_class', 'host_name', 'chaddr']):

        # uncomment next line to print full details
        # print packet.str()

        for option in options:
            # chaddr is not really and option, it's in the fixed header
            if option == 'chaddr':
                begin = DhcpFields[option][0]
                end = begin+6
                opdata = packet.packet_data[begin:end]
                hex = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
                print option+':', ':'.join([(hex[i/16]+hex[i%16]) for i in opdata])
            else:
                opdata = packet.options_data.get(option)
                if opdata:
                    print option+':', ''.join([chr(i) for i in opdata if i != 0])
        print

    def SaveHost(self, packet):
	opdata = packet.options_data.get('host_name')
	hostn = ''.join([chr(i) for i in opdata if i != 0])
	print hostn


    def HandleDhcpDiscover(self, packet):
        print "DHCP DISCOVER"
        self.PrintOptions(packet)
	self.SaveHost(packet)
    def HandleDhcpRequest(self, packet):
        print "DHCP REQUEST"
        self.PrintOptions(packet)
        self.SaveHost(packet)

    ##  def HandleDhcpDecline(self, packet):
    ##      self.PrintOptions(packet)
    ##  def HandleDhcpRelease(self, packet):
    ##      self.PrintOptions(packet)
    ##  def HandleDhcpInform(self, packet):
    ##      self.PrintOptions(packet)


server = Server(netopt)

while True :
    server.GetNextDhcpPacket()
