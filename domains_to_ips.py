#!/usr/bin/env python
import socket
import sys

def displayUsage():
    print("python domains_to_ips.py HOSTNAMES_FILE.txt")

def getIP(hostname):
    try:
        print(hostname + " " + socket.gethostbyname(hostname))
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        displayUsage()
        sys.exit(-1)

    args = sys.argv[1:]
    infile_name = sys.argv[1]
    infile = open(infile_name,"r")
    hostnames = infile.readlines()
    infile.close

    for hostname in hostnames:
        getIP(hostname.strip())
