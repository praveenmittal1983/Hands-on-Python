from logger_setup import LoggerSetup
import configparser

logger = LoggerSetup.get_logger()

class Config:
    def __init__(self, locale):
        try:
            logger.info("Initializing Config with locale %s", locale)
            self.config = configparser.ConfigParser()
            if not self.config.read("config.ini"):
                raise FileNotFoundError("Configuration file 'config.ini' not found")
            self.config = self.config[locale]
        except KeyError as e_msg:
            raise RuntimeError(f"Failed process config file with error: {e_msg}") from e_msg