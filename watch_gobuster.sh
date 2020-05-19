#!/bin/bash
for file in `ls -lart | awk '{if ($5 != 0) print $9}' | grep txt | grep -v interlace`; do cat $file | grep "Status: 200";done | tail -50
