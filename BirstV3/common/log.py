import logging, logging.config
import yaml

def setLoggerContext(fileName, env):
    with open(fileName, 'r') as f:
        log_Configuration = yaml.safe_load(f.read())

    logging.config.dictConfig(log_Configuration)
    return logging.getLogger(env)

## Testing
# # logger = logging.getLogger('dev')
# # logger.setLevel(logging.INFO)
# logger = setLoggerContext('.\\config\\log.yaml','dev')

# logger.info('This is an info message')
# logger.error('This is an error message')
# logger.debug('This is an debug message')
