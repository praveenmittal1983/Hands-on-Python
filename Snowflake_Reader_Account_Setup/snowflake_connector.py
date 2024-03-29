from logger_setup import LoggerSetup
from config import Config
import snowflake.connector

logger = LoggerSetup.get_logger()

class SnowflakeConnector(Config):
    _instance = None

    def __new__(cls, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, locale, reader_account={}, print_only=True) -> None:
        logger.info("Initializing Snowflake Connection")
        super().__init__(locale)

        try:
            if len(reader_account) == 0:
                self._conn = snowflake.connector.connect(
                    user=self.config['user'],
                    password=self.config['password'],
                    account=self.config['account'],
                    warehouse=self.config['warehouse'],
                    role='ACCOUNTADMIN'
                )
            else:
                self._conn = snowflake.connector.connect(
                    user=reader_account['admin_user'] if 'admin_user' in reader_account else None,
                    password=reader_account['admin_password'] if 'admin_password' in reader_account else None,
                    account=reader_account['login_account'] if 'login_account' in reader_account else None,
                    role='ACCOUNTADMIN'
                )

            self._cursor = self._conn.cursor()
        except RuntimeError as e_msg:
            raise RuntimeError(f"Failed to connect Snowflake: {e_msg}") from e_msg
        except snowflake.connector.errors.ProgrammingError as e_msg:
            raise RuntimeError(f"Failed to connect Snowflake: {e_msg}") from e_msg
        except snowflake.connector.errors.DatabaseError as e_msg:
            raise RuntimeError(f"Failed to connect Snowflake: {e_msg}") from e_msg
        
        if not self._cursor:
            raise RuntimeError("Failed to connect Snowflake")

        self.params = {}
        ext_client_name = self.config['ext_client_name'].upper().strip()
        self.params['ext_client_name'] = ext_client_name
        self.params['ext_client_id'] = None

        self.params['config_db'] = self.config['config_db']
        self.params['config_schema'] = self.config['config_schema']
        
        self.params['primary_db'] = self.config['primary_db']
        self.params['primary_schema'] = self.config['primary_schema']
        self.params['context_id'] = self.config['context_id']
        self.params['context_names'] = self.config['context_names']
        self.params['primary_ignore_tables'] = self.config['primary_ignore_tables']

        self.params['flash_db'] = self.config['flash_db']
        self.params['flash_schema'] = self.config['flash_schema']
        self.params['event_owner_id'] = self.config['event_owner_id']
        self.params['event_owner_names'] = self.config['event_owner_names']
        self.params['flash_ignore_tables'] = self.config['flash_ignore_tables']
        
        self.params['reader_account_db_name'] = self.config['reader_account_db_display_name']
        self.params['reader_account_admin_email'] = self.config['reader_account_admin_email']
        self.params['print_only'] = print_only

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Exit Snowflake")
        self._cursor.close()

    def execute(self, sql, params=None, print_only=True):
        try:
            logger.debug(sql)
            if not print_only:
                return self._cursor.execute(sql, params or ())
        except snowflake.connector.errors.ProgrammingError as e_msg:
            raise RuntimeError(f"Failed while running SQL {sql} with error {e_msg}") from e_msg