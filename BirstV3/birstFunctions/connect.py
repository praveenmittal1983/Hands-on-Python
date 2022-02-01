import zeep
from common import timeDecorator

class Birst:

    timeDecorator.TimingBenchmark.enable(False)

    def __init__(self, logger, wsdl, username, password):
        self.logger = logger
        self.client = zeep.Client(wsdl=wsdl)
        self.username = username
        self.password = password
        self.token = self.Login()

    @timeDecorator.TimingBenchmark()
    ## Login Module
    def Login(self):
        token = self.client.service.Login(self.username, self.password)
        return token

    @timeDecorator.TimingBenchmark()
    ## Logout Module
    def Logout(self):
        ## For some reason token is not None (not working)
        if not self.token:
            self.client.service.Logout(self.token)
        return 0

    ## Not in use (Older Implementation) 
    # @timeDecorator.TimingBenchmark()
    # def runBQL(self, spaceID, bql):
    #     #Run BQL Query to get all Birst Users in Security Table
    #     #Check if User exist in Birst
    #     #Get their Language

    #     data = []
    #     queryResult = self.client.service.executeQueryInSpace(self.token, bql, spaceID)
    #     # logger.debug("QueryResults: {}".format(queryResult))

    #     # for index, item in enumerate(queryResult['rows']['ArrayOfString']):
    #     #     username = item['string'][0]
    #     #     userLanguage = None

    #     #     #Get Language
    #     #     try:
    #     #         userLanguage = client.service.getLanguageForUser(loginToken,username)
    #     #         item['string'].append(userLanguage)
    #     #         data.append({
    #     #             'Username' : username,
    #     #             'Language': userLanguage
    #     #             })
    #     #     except Exception as e:
    #     #         logger.info('Username {} does not exist'.format(username))
    #     #         logger.debug('StackTrace: {}'.format(e))

    #     # ## Creating the file with release definition details
    #     # fileOperations.write2File(r'data//Users_with_Language.json',json.dumps(data))


    @timeDecorator.TimingBenchmark()
    def getSpaces(self):
        return self.client.service.listAllSpaces(self.token);

    @timeDecorator.TimingBenchmark()
    def getAllHierarchies(self, spaceID):
        return self.client.service.getAllHierarchies(self.token, spaceID);

    @timeDecorator.TimingBenchmark()
    def listCreatedUsers(self):
        return self.client.service.listCreatedUsers(self.token);

    @timeDecorator.TimingBenchmark()
    def listGroupsInSpace(self, spaceID):
        return self.client.service.listGroupsInSpace(self.token, spaceID);

    @timeDecorator.TimingBenchmark()
    def listCustomSubjectAreas(self, spaceID):
        return self.client.service.listCustomSubjectAreas(self.token, spaceID);

    @timeDecorator.TimingBenchmark()
    def getSourcesList(self, spaceID):
        return self.client.service.getSourcesList(self.token, spaceID);

    @timeDecorator.TimingBenchmark()
    def listCloudConnections(self, spaceID):
        return self.client.service.listCloudConnections(self.token, spaceID);        