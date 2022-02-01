import configparser

class MyConfig(object):

    def __init__(self, file_name):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)
        if not self.config.sections():
            raise ValueError('Config file [{}] not found!'.format(file_name))

    def __getitem__(self, key):
        if not self.config.has_option(key[0],key[1]):
            raise ValueError('Key [{} - {}] not found'.format(key[0], key[1]))
        return self.config[key[0]][key[1]]

    def __del__(self):
        del self.config

## Testing
# config = MyConfig('..\config\config.ini')
# print (config['DEFAULT','WSDL'])