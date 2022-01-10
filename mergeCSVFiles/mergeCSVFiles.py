import pandas
import sys, os, subprocess, re
import datetime

EXPECTED_NO_OF_COLUMNS = 3
OUTPUT_FILENNAME = "output.csv"

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
    datefromData = datetime.datetime.strptime(data.iloc[0].values[0], '%m/%d/%Y').strftime("%m%d%Y")
    if len(datefromFileName) > 0 and datefromFileName[0] != datefromData:
        print ("Skipping file {} due to failure in filename format and date {} from data validation.".format(filename, datefromData))
        return False

    return True

# Keep track of raw count
def line_count(filename):
    return sum(1 for line in open(filename, mode='r', encoding='ISO-8859-1'))

# Looks for csv file and merge them
def get_and_merge_csv_files(path):	
    list_df = []
    total_line_count = 0
    for file in os.listdir(path):
        if file.endswith(".csv"):
            df = pandas.read_csv(path + "\\" + file, encoding= 'unicode_escape')
            if validateFile(file, df.iloc[[0, -1]], len(df.columns)):
                total_line_count += line_count(path + "\\" + file)
                list_df.append(df)
    if len(list_df) > 0:
        pandas.concat(list_df).to_csv(OUTPUT_FILENNAME, index=False)
        print ("Total raw count from actual file is {} and merged file is {}".format(total_line_count, line_count(OUTPUT_FILENNAME)))
    else:
        print ("No files found to merge")
        
if __name__ == "__main__":
    inputPath = sys.argv[1]
    if validatePath(inputPath):
        get_and_merge_csv_files(inputPath);
    else:
        print ("Invalid Argument: Please provide a valid directory")