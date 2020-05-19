#!/usr/bin/env python

import sys

def displayUsage():
    print("python delimited_payloads.py INFILE.txt DELIMITER WORDLIST.txt")
    print("")
    print("Use for stuff like '5554|222|1|999|xxx' that is base64-encoded then submitted in an HTTP request to a web application")


# For each key-value pair in the input json file, replace the value with each word from the input wordlist and print to stdout
def replaceValues(lines, delim, words):
    for line in lines:
        strings = line.split(delim)
        for index, item in enumerate(strings):
            for word in words:
                outStrings = strings.copy()
                outStrings[index] = word
                print(delim.join(outStrings))


if __name__ == "__main__":

    # Check system arguments
    if len(sys.argv)<3:
        displayUsage()
        sys.exit(-1)

    # Get file contents
    args = sys.argv[1:]
    inFileName = args[0]
    with open(inFileName) as inFile:
        lines = inFile.readlines()
    lines = [line.strip() for line in lines]
    
    # Set delimiter
    delim = args[1]

    # Get wordlist contents
    wordlistFileName = args[2]
    wordlistFile = open(wordlistFileName,"r")
    words = wordlistFile.readlines()
    words = [word.strip() for word in words]
    wordlistFile.close

    replaceValues(lines, delim, words)

