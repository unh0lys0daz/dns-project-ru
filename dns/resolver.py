#!/usr/bin/env python3

"""DNS Resolver

This module contains a class for resolving hostnames. You will have to implement
things in this module. This resolver will be both used by the DNS client and the
DNS server, but with a different list of servers.
"""


import socket

from dns.classes import Class
from dns.message import Message, Question, Header
from dns.name import Name
from dns.types import Type
from dns.resource import ResourceRecord
from dns.cache import RecordCache

class Resolver:
    """DNS resolver"""

    def __init__(self, timeout, caching, ttl, rd):
        """Initialize the resolver

        Args:
            caching (bool): caching is enabled if True
            ttl (int): ttl of cache entries (if > 0)
        """
        self.timeout = timeout
        self.caching = caching
        self.ttl = ttl
        self.rd = rd

    def gethostbyname(self, hostname, dnsserv):
        """Translate a host name to IPv4 address.

        Currently this method contains an example. You will have to replace
        this example with the algorithm described in section 5.3.3 in RFC 1034.

        Args:
            hostname (str): the hostname to resolve

        Returns:
            (str, [str], [str]): (hostname, aliaslist, ipaddrlist)
        """
        ipaddrlist = []
        cnames = []
        temp = []
        if(self.caching):
            rcache = RecordCache(ttl)
            rcord = rcache.lookup(hostname, Type.ANY, Class.IN)
            if(rcord):
                for rec in rcord:
                    if rec.type_ == Type.A:
                        arec = rec.rdata
                        ipaddrlist = ipaddrlist + arec.address
                    elif rec.type_ == Type.CNAME:
                        crec = rec.rdata
                        cnames = cnames + crec.cname
            if ipaddrlist:
                return hostname, cnames, ipaddrlist
            elif cnames:
                for cname in cnames:
                    (host, aliases, ipaddrl) = self.gethostbyname(cname)
                    if ipaddrl:
                        return (host, aliases, ipaddrl)
                    elif aliases:
                        cnames = cnames + aliases
        
        

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        # Create and send query
        question = Question(Name(hostname), Type.A, Class.IN)
        header = Header(9001, 0, 1, 0, 0, 0)
        header.qr = 0
        header.opcode = 0
        header.rd = 1
        query = Message(header, [question])
        sock.sendto(query.to_bytes(), (dnsserv, 53))

        # Receive response
        data = sock.recv(512)
        response = Message.from_bytes(data)

        # Get data
        aliaslist = []
        ipaddrlist = []
        for answer in response.answers:
            if answer.type_ == Type.A:
                ipaddrlist.append(answer.rdata.address)
            if answer.type_ == Type.CNAME:
                aliaslist.append(hostname)
                hostname = str(answer.rdata.cname)
            if answer.type == Type.NS:
        if ipaddrlist:
            return hostname, aliaslist, ipaddrlist
        if aliaslist:
            for name in aliaslist:

