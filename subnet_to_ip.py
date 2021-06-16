#!/usr/bin/env python

from netaddr import IPNetwork
for ip in IPNetwork('10.113.0.0/16'):
    print '%s' % ip
