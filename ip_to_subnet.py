#!/usr/bin/env python3

import argparse
import ipaddress
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

parser = argparse.ArgumentParser(description="Check validity of reference links in Excel spreadsheets.")
parser.add_argument("csvfile")
parser.add_argument("subnetfile")

args = parser.parse_args()

with open(args.csvfile) as csvfile, open(args.subnetfile) as subnetfile:
    subnets = [ s.strip() for s in subnetfile ]
    for row in csvfile:
        for net in subnets:
            ip = row.strip()
            if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(net, strict=False):
                print(",".join((ip, net)))
                break