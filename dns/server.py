#!/usr/bin/env python3

"""A recursive DNS server

This module provides a recursive DNS server. You will have to implement this
server using the algorithm described in section 4.3.2 of RFC 1034.
"""


from threading import Thread
from dns.message import Message
from dns.zone import Zone
from dns.zone import Catalog

class RequestHandler(Thread):
    """A handler for requests to the DNS server"""

    def __init__(self, data, addr):
        """Initialize the handler thread"""
        super().__init__()
        self.daemon = True
        self.data = data
        self.addr = addr

    def run(self):
        """ Run the handler thread"""
        msg = Message.from_bytes(self.data)
        header = msg.header
        recursion = header.rd() != 0
        questions = msg.questions
        for question in questions:






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
            handler = RequestHandler(data, addr, zone)
            handler.run()

            

    def shutdown(self):
        """Shut the server down"""
        self.done = True
