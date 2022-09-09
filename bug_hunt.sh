#!/bin/bash

# Uses a list of individual IP addresses as the first argument and returns recon files
if [ "$#" -ne 1 ] || ! [ -f "$1" ]; then
    echo "Usage: $0 IP_FILENAME" >&2
    exit 1
fi

# Splitting subnets into individual IP addresses in a file
python3 ~/scripts-tmp/cidr_to_ip.py $1 > ips.txt

# Perform reverse DNS resolution on provided IP addresses
echo "Performing reverse DNS resolution to enumerate domain names..."
for ip in $(cat ips.txt); do host $ip | grep pointer | awk '{print $5}' | rev | cut -d . -f2- | rev | tee /dev/tty >> domains_revdns.txt; done
cat domains_revdns.txt | sort -u | sponge domains_revdns.txt

# Query DNS resolvers for known subdomains
for root in `cat domains_revdns.txt`; do echo $root | rev | cut -d . -f1,2 | rev | tee /dev/tty >> domains_rootdomains.txt; done
cat domains_rootdomains.txt | sort -u | sponge domains_rootdomains.txt
echo "Running assetfinder on discovered root domain names to enumerate subdomains..."
for domain in `cat domains_rootdomains.txt`; do assetfinder $domain | tee /dev/tty >> domains_assetfinder.txt; done
cat domains_assetfinder.txt | sort -u | sponge domains_assetfinder.txt

# Resolve discovered subdomains back to IP addresses and check if they are in-scope
echo "Performing forward DNS resolution on discovered subdomain names to remove out-of-scope targets..."
for domain in `cat domains_assetfinder.txt`; do host $domain | grep 'has address' | awk '{print $1,$4}' | tee /dev/tty >> domains_assetfinder_resolved.txt; done
for ip in `cat ips.txt`; do grep "$ip$" domains_assetfinder_resolved.txt | tee /dev/tty >> domains_assetfinder_inscope_ips.txt; done
cat domains_assetfinder_inscope_ips.txt | sort -u | sponge domains_assetfinder_inscope_ips.txt
cat domains_assetfinder_inscope_ips.txt | cut -d " " -f1 >> inscope_domains.txt

# Run httprobe on in-scope domains
echo "Identifying HTTP/HTTPS ports on in-scope domain names..."
cat inscope_domains.txt | httprobe | tee /dev/tty > inscope_urls.txt

# Run meg on web root for in-scope URLs
echo "Capturing HTTPS responses for each in-scope URL web root..."
meg / inscope_urls.txt

# Run content discovery scans


#echo "Running amass on discovered root domain names..."
#amass enum -active -brute -df domains_rootdomains.txt -ipv4 -json domains_amass.json -o domains_amass.txt &

