#!/usr/bin/python3
import ipaddress, sys

target = sys.argv[1]
prefix = int(sys.argv[2])

for subnet in ipaddress.ip_network(target).subnets(new_prefix=prefix):
    print(subnet)
