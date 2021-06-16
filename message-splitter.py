#!/usr/bin/python3

import sys
import json
from urllib.parse import unquote, quote

DELIM = "§"

def addDelims(inData):
    if type(inData) == type("string"):
        return DELIM + inData + DELIM
    elif type(inData) == type({'a':'b'}):
        outData = {}
        for k,v in inData.items():
            outData[k] = addDelims(v)
        return outData
    elif type(inData) == type([1,2,3]):
        outData = []
        for i in inData:
            outData.append(addDelims(i))
        return outData

data = sys.argv[1]

dataDict = json.loads(unquote(data))

outData = addDelims(dataDict)

output = quote(json.dumps(outData, ensure_ascii=False)).replace("%C2%A7", DELIM)

print()
print(output)
