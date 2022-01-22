import sys, os, subprocess

# Program to run a Shell command against each csv file in a directory
# This was needed to run a utility (CSVManipulator_OutputFile_WithDate.jar) against multiple files (~200 files).
# Command to run program: python .\runCommand.py "directory_path_containing_csv"

# Valid InputPath is valid directory
def validatePath(path):
    return os.path.isdir(path)

def runCommand(path):
    print ("Running command for all csv files in path [{}]".format(inputPath))
    for file in os.listdir(path):
        if file.endswith(".csv"):
            p = subprocess.run(["java", "-jar", "C:\sample\CSVManipulator_OutputFile_WithDate.jar", path + '\\' + file], shell=True, capture_output=True)
            print(p.stdout.decode(), p.stderr.decode())
    
if __name__ == "__main__":
    
    inputPath = ""
    if len(sys.argv) > 1:
        inputPath = sys.argv[1]

    if validatePath(inputPath):
        runCommand(inputPath);
    else:
        print ("Invalid Argument: Please provide a valid directory")    