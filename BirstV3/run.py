
import sys, json, log
import argparse, traceback
from zeep.helpers import serialize_object
from common import config, fileOperations, log, timeDecorator
from birstFunctions import connect

## Setup logging
logger = log.setLoggerContext('.\\config\\log.yaml','dev')

## Turning Trace Off and Benchmark
# sys.tracebacklimit = 0
timeDecorator.TimingBenchmark.enable(True)
timeDecorator.TimingBenchmark.setLogger(logger)

# @timeDecorator.TimingBenchmark()
def processArgs():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--listallspaces', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--listCreatedUsers', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--getAllHierarchies', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--listGroupsInSpace', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--listCustomSubjectAreas', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--getSourcesList', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--listCloudConnections', default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args  

## Main
if __name__ == "__main__":

    args = processArgs()
    logger.info("Starting application {}".format(__name__))

    ## Initializing variables
    config = config.MyConfig('.//config//config.ini')

    try:
        ## Creating a session with Birst via Birst Web-Service
        birstObj = connect.Birst(logger, config['DEFAULT','WSDL'], config['DEFAULT','Username'], config['DEFAULT','Password'])

        ## Calling Birst API based on argument passed
        if args.listallspaces: 
            response = json.dumps(serialize_object(birstObj.getSpaces()))
            fileOperations.writeJson2CSVFile("data\\listallspaces.csv", response)

        if args.listCreatedUsers:
            response = json.dumps(serialize_object(birstObj.listCreatedUsers()))
            fileOperations.writeJson2CSVFile("data\\listCreatedUsers.csv", response)

        if args.getAllHierarchies:
            response = json.dumps(serialize_object(birstObj.getAllHierarchies(config['Space','ID'])))
            fileOperations.writeJson2CSVFile("data\\getAllHierarchies.csv", response)

        if args.listGroupsInSpace:
            response = json.dumps(serialize_object(birstObj.listGroupsInSpace(config['Space','ID'])))
            fileOperations.writeJson2CSVFile("data\\listGroupsInSpace.csv", response)

        if args.listCustomSubjectAreas:
            response = json.dumps(serialize_object(birstObj.listCustomSubjectAreas(config['Space','ID'])))
            fileOperations.writeJson2CSVFile("data\\listCustomSubjectAreas.csv", response)

        if args.getSourcesList:
            response = json.dumps(serialize_object(birstObj.getSourcesList(config['Space','ID'])))
            fileOperations.writeJson2CSVFile("data\\getSourcesList.csv", response)

        if args.listCloudConnections:
            response = json.dumps(serialize_object(birstObj.listCloudConnections(config['Space','ID'])))
            fileOperations.write2File("data\\listCloudConnections.txt", response)

    except Exception as eMsg:
        logger.error(traceback.format_exc())
        logger.error('Exception: {}'.format(str(eMsg)))
    finally:
        birstObj.Logout()
        logger.info('Successfully Logout from the application')