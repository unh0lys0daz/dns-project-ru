#!/usr/bin/env python3

"""A recursive DNS server

This module provides a recursive DNS server. You will have to implement this
server using the algorithm described in section 4.3.2 of RFC 1034.
"""


from threading import Thread
from dns.message import Message
from dns.zone import Zone
from dns.zone import Catalog
from dns.resolver import Resolver

class RequestHandler(Thread):
    """A handler for requests to the DNS server"""

    def __init__(self, data, addr, sock):
        """Initialize the handler thread"""
        super().__init__()
        self.daemon = True
        self.data = data
        self.addr = addr
        self.sock = sock

    def run(self):
        """ Run the handler thread"""
        msg = Message.from_bytes(self.data)
        header = msg.header
        recursion = header.rd() != 0
        questions = msg.questions
        for question in questions:
            #FIXME if not in zone blabla
            if recursion:
                answers = []
                resolver = Resolver(100, False, 0, True)
                (hostname, aliaslist, ipaddrlist) = resolver.gethostbyname(question.qname)
                header_response = Header(9001, 0, 1, len(aliaslist) + len(ipaddrlist), 0, 0)
                header_response.qr(1)
                header_response.opcode(1)
                header_response.aa(0)
                header_respones.tc(0)
                header_response.rd(0)
                header_response.ra(1)
                header_response.z(0)
                header_respones.rcode(0)

                for addr in ipaddrlist:
                    answers.append(ResourceRecord.from_dict(
                        { "name" : str(hostname) ,
                          "type" : str(Type.A) ,
                          "class": str(Class.IN) ,
                          "ttl"  : "0",
                          "rdata": { "address" : addr } } )
                for alias in aliaslist:
                    answers.append(ResourceRecord.from_dict(
                        { "name" : str(hostname) ,
                          "type" : str(Type.CNAME) ,
                          "class": str(Class.IN) ,
                          "ttl"  : "0",
                          "rdata": { "cname" : str(alias) } } )
                response = Message(header_response, questions, answers)
                self.sock.sendto(response.to_bytes, self.addr)



        
            






class Server:
    """A recursive DNS server"""

    def __init__(self, port, caching, ttl):
        """Initialize the server

        Args:
            port (int): port that server is listening on
            caching (bool): server uses resolver with caching if true
            ttl (int): ttl for records (if > 0) of cache
        """
        self.caching = caching
        self.ttl = ttl
        self.port = port
        self.done = False

    def serve(self):
        """Start serving requests"""
        zone = Zone()
        zone.read_master_file('zone')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1',self.port))
        sock.listen(10)
        while not self.done:
            data, addr = sock.recvfrom(65000) 
            handler = RequestHandler(data, addr, zone, sock)
            handler.start()

            

    def shutdown(self):
        """Shut the server down"""
        self.done = True
