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

    def getnsaddr(self, nsname, additionals):
        for rr in additionals:
            print(rr.name + " " + nsname)
            if rr.name == nsname and rr.type_ == Type.A:
                return rr.rdata.address
        return None

    def gethostbyname(self, hostname, dnsserv='192.112.36.4'):
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
                return self.gethostbyname(cnames[0], dnsserv)
        

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
        data = sock.recv(2048)
        response = Message.from_bytes(data)
        print("Number of answers: " +str(len(response.answers)))
        print("Number of authorities: " + str(len(response.authorities)))
        print("Number of additionals: " + str(len(response.additionals)))

        # Get data
        aliaslist = cnames
        ipaddrlist = []
        dnslist = []
        
        while response.answers:
            for answer in response.answers:
                if answer.type_ == Type.A:
                    ipaddrlist.append(answer.rdata.address)
                if answer.type_ == Type.CNAME:
                    aliaslist.append(answer.rdata.cname)
                if answer.type == Type.NS:
                    dnslist.append(answer.rdata.nsdname)
            if ipaddrlist:
                return hostname, aliaslist, ipaddrlist
            elif aliaslist:
                question = Question(Name(aliaslist[0]), Type.A, Class.IN)
                query = Message(header, [question])
                sock.sendto(query.to_bytes(), (dnsserv, 53))
                data = sock.recv(2048)
                response = Message.from_bytes(data)
            elif dnslist:
                nsname = dnslist.pop()
                maybe_dnsserv = self.getnsaddr(nsname, response.additionals)
                if maybe_dnsserv:
                    dnsserv = maybe_dnsserv
                else:
                    pass
                sock.sendto(query.to_bytes(), (dnsserv, 53))
                data = sock.recv(2048)
                response = Message.from_bytes(data)
            else:
                break

        if response.authorities:
            for authority in response.authorities:
                if authority.type_ != Type.NS:
                    pass
                dnslist.append(answer.rdata.nsdname)
            while dnslist:
                nsname = dnslist.pop()
                maybe_next_dnsserv = self.getnsaddr(nsname, response.additionals)
                if maybe_next_dnsserv:
                    next_dns_serv = maybe_next_dnsserv
                else:
                    pass
                (hname, aliasl, ipaddrl) = self.gethostbyname(hostname, nsname)
                if ipaddrl:
                    return hname, aliasl, ipaddrl

        
        
        
        
        for answer in response.answers:
            print("****")
            if answer.type_ == Type.A:
                print("found A: " + str(answer.name) + " " + answer.rdata.address)
                ipaddrlist.append(answer.rdata.address)
            if answer.type_ == Type.CNAME:
                print("found CNAME: " + str(answer.rdata.cname))
                aliaslist.append(str(answer.rdata.cname))
            if answer.type == Type.NS:
                print("found NS: " + str(answer.rdata.nsdname))
                dnslist.append(str(answer.rdata.nsdname))

        if ipaddrlist:
            return hostname, aliaslist, ipaddrlist
        if aliaslist:
            return self.gethostbyname(aliaslist[0], dsnserv)
        if dnslist:
           for ns in dnslist:
               for answer in response.answers:
                   if answer.name == ns and answer.type_ == Type.A:
                       dnsserv = answer.rdata.address
               (hostn, aliasl, ipaddrl) = self.gethostbyname(hostname, dnsserv)
               if ipaddrl:
                   return hostn, aliasl, ipaddrl
               if aliasl:
                   return self.gethostbyname(hostn, dnsserv)
        return None, None, None
