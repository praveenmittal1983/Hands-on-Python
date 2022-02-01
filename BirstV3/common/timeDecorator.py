import time
from common import log

class TimingBenchmark:
    enabled = False

    @classmethod
    def enable(cls, value):
        ''' Use this function to enable/disable TimingBenchmark 
        '''
        cls.enabled = value

    @classmethod
    def setLogger(cls, logger):
        ''' Setting up Logging on Initializing
        '''
        cls.logger = logger

    @classmethod
    def __init__(cls):
        ''' Setting up Logging on Initializing
        '''
        # cls.logger = log.setLoggerContext()

    @classmethod
    def __call__(cls, func):
        ''' This function calculate the time taken by function to complete its execution.
            func: Name of the function for which execution timing to be tracked
        '''
        if cls.enabled == False:
            return func
        
        def wrapper(*args, **kwargs):
            startTime = time.time()
            func(*args, **kwargs)
            endTime = time.time()
            cls.logger.debug('Module: {} took: {} seconds'.format(func.__name__, endTime - startTime))

        return wrapper

    @classmethod
    def __del__(cls):
        ''' Freeup class
        '''
        # del cls.logger