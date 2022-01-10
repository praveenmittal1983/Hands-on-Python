import pandas
import os
import sys
import datetime
import re

EXPECTED_NO_OF_COLUMNS = 3

# Valid InputPath is valid directory
def validatePath(inputPath):
    return os.path.isdir(inputPath)

# File validation
def validateFile(filename, data, noOfColumns):

    # Verify number of columns matches
    if EXPECTED_NO_OF_COLUMNS != noOfColumns:
        print ("Skipping file {} due to failure in column match condition. Expected was {} but received {}".format(filename, EXPECTED_NO_OF_COLUMNS, noOfColumns))
        return False
    
    # Verify first row and last row starts with same value
    if data.iloc[0].values[0] != data.iloc[1].values[0]:
        print ("Skipping file {} due to failure in matching first and last row. First row value is {} and last row value is {}".format(filename, data.iloc[0].values[0], data.iloc[1].values[0]))
        return False
    
    # Verify first row starts with valid date with valid format
    if not bool(datetime.datetime.strptime(data.iloc[0].values[0], '%m/%d/%Y')):
        print ("Skipping file {} due to failure in date check format. First row value is {}".format(filename, data.iloc[0].values[0]))
        return False

    # Verify filename format
    datefromFileName = re.findall(r'\d+', filename)
    if len(datefromFileName) > 0 and datefromFileName[0] != data.iloc[0].values[0].replace('/', ''):
        print ("Skipping file {} due to failure in filename format.".format(filename))
        return False

    return True

# Looks for csv file and merge them
def get_and_merge_csv_files(path):	
    list_df = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            df = pandas.read_csv(path + "\\" + file)
            if validateFile(file, df.iloc[[0, -1]], len(df.columns)):
                print (df)
                list_df.append(df)
    if len(list_df) > 0:
        pandas.concat(list_df).to_csv( "output.csv", index=False)
    else:
        print ("No files found to merge")
        
if __name__ == "__main__":
    inputPath = sys.argv[1]
    if validatePath(inputPath):
        get_and_merge_csv_files(inputPath);
    else:
        print ("Invalid Argument: Please provide a valid directory")