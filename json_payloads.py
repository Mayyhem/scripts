#!/usr/bin/env python

import json, sys

def displayUsage():
    print("python json_payloads.py JSON_INFILE.json WORDLIST.txt")

# For each key-value pair in the input json file, replace the value with each word from the input wordlist and print to stdout
def replaceKeyValues(jsonData, words):
    for key, value in jsonData.items():
        for word in words:
            jsonData[key] = word.strip()
            print(json.dumps(jsonData))
            jsonData[key] = value

if __name__ == "__main__":

    # Check system arguments
    if len(sys.argv)<3:
        displayUsage()
        sys.exit(-1)

    # Get file contents
    args = sys.argv[1:]
    jsonFileName = args[0]
    with open(jsonFileName) as jsonFile:
        jsonData = json.load(jsonFile)
    wordlistFileName = args[1]
    wordlistFile = open(wordlistFileName,"r")
    words = wordlistFile.readlines()
    wordlistFile.close

    replaceKeyValues(jsonData, words)

