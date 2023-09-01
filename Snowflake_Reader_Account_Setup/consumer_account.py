from logger_setup import LoggerSetup
from snowflake_connector import SnowflakeConnector

logger = LoggerSetup.get_logger()

class SetupConsumerAcount(SnowflakeConnector):
    def __init__(self, locale, reader_account, reader_user, reader_user_credentials, client_details, print_only=True) -> None:
        logger.info("Module: Setup Consumer Account")
        super().__init__(locale, reader_account=reader_account, print_only=print_only)
        self.params['ext_client_id'] = client_details['ext_client_id'] # Updating External Client ID which was received from the Mapping Table

        self.reader_account_details = {}
        self.reader_account_details['url'] = reader_account['url']
        self.reader_account_details['admin_user'] = reader_account['admin_user']
        self.reader_account_details['admin_password'] = reader_account['admin_password']
        self.reader_account_details['ext_username'] = f"EXT_USER_CLIENT_ID_{self.params['ext_client_id']}" if not reader_user else reader_user
        self.reader_account_details['ext_password'] = reader_user_credentials
        self.reader_account_details['ext_db_name'] = self.params['reader_account_db_name'] if self.params['reader_account_db_name'] else self.params['ext_client_name']

    def run(self):
        v = self.params
        r = self.reader_account_details
        print_only = self.params['print_only']

        self.execute('Use role ACCOUNTADMIN', print_only=False)
        self.execute(self.common['sql_alter_reader_account_admin'].format(**v, **r), print_only=print_only)
        self.execute(self.common['sql_create_rmonitor'].format(**v), print_only=print_only)
        self.execute(self.common['sql_create_warehouse'].format(**v), print_only=print_only)
        self.execute(self.common['sql_create_role'].format(**v), print_only=print_only)
        self.execute(self.common['sql_create_user'].format(**v, **r), print_only=print_only)
        self.execute(self.common['sql_grant_role_to_user'].format(**v, **r), print_only=print_only)
        self.execute(self.common['sql_grant_role_to_warehouse'].format(**v), print_only=print_only)
        self.execute(self.common['sql_create_db'].format(**v, **r), print_only=print_only)
        self.execute(self.common['sql_grant_role_to_db'].format(**v, **r), print_only=print_only)
        
        logger.info(f"Setup of Consumer Account for external client {v['ext_client_name']} completed. Details: {self.reader_account_details}")