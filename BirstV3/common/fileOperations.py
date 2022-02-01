import sys, json
import pandas as pd

## Writing string to a file
def write2File(filename, data):
    with open(filename, 'wt') as fileObject:
        fileObject.write(data)
        fileObject.close()

## Writing List to a file
def writeList2File(filename, data):
    with open(filename, 'wt') as fileObject:
        fileObject.writelines("%s\n" % row for row in data)
        fileObject.close()

## Reading from a file
def readFile(filename, data):
    with open(filename, 'wt') as fileObject:
        fileObject.write(data)
        fileObject.close()

## Write JSON to CSV File
def writeJson2CSVFile(filename, data):
    df = pd.read_json(data)
    df.to_csv(filename, encoding='utf-8', index=False)