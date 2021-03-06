#!/usr/bin/env python3

"""A cache for resource records

This module contains a class which implements a cache for DNS resource records,
you still have to do most of the implementation. The module also provides a
class and a function for converting ResourceRecords from and to JSON strings.
It is highly recommended to use these.
"""


import json

from dns.resource import ResourceRecord
from dns.types import Type


class RecordCache:
    """Cache for ResourceRecords"""

    def __init__(self, ttl):
        """Initialize the RecordCache

        Args:
            ttl (int): TTL of cached entries (if > 0)
        """
        self.records = []
        self.ttl = ttl

    def lookup(self, dname, type_, class_):
        """Lookup resource records in cache

        Lookup for the resource records for a domain name with a specific type
        and class.

        Args:
            dname (str): domain name
            type_ (Type): type
            class_ (Class): class
        """
        found = []
        self.read_cache_file()
        for record in self.records:
            print("UGH")
            if str(dname) == str(record.name) and (type_ == record.type_ or type_ == Type.ANY) and class_ == record.class_:
                if record not in found:
                    found.append(record)
        return found

    def add_record(self, record):
        """Add a new Record to the cache

        Args:
            record (ResourceRecord): the record added to the cache
        """
        self.read_cache_file()
        self.records.append(record)
        self.write_cache_file()

    def read_cache_file(self):
        """Read the cache file from disk"""
        dcts = []
        try:
            with open("cache", "r") as file_:
                dcts = json.load(file_)
        except:
            print("could not read cache")
        self.records = [ResourceRecord.from_dict(dct) for dct in dcts]

    def write_cache_file(self):
        """Write the cache file to disk"""
        print("We're caching")
        dcts = [record.to_dict() for record in self.records]
        try:
            with open("cache", "w") as file_:
                json.dump(dcts, file_, indent=2)
        except:
            print("could not write cache")
