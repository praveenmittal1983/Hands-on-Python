import json
from logger_setup import LoggerSetup
from snowflake_connector import SnowflakeConnector
import sys

logger = LoggerSetup.get_logger()

class SetupProviderAcount(SnowflakeConnector):
    def __init__(self, locale, reader_admin, reader_admin_credentials, client_details, print_only=True) -> None:
        logger.info("Module: Setup Provider Account")
        super().__init__(locale, print_only=print_only)
        self.reader_account_details = {}
        self.reader_account_details['admin_user'] = reader_admin
        self.reader_account_details['admin_password'] = reader_admin_credentials
        # self.client_details = client_details

        self.reader_account_details['account_name'] = client_details['reader_account_name']
        self.reader_account_details['account'] = client_details['reader_account_id']
        self.params['ext_client_id'] = client_details['ext_client_id'] # Updating External Client ID which was received from the Mapping Table

    def create_reader_account(self, user, password):
        account_name = None
        url = None
        result_set = self.execute(self.common['sql_create_managed_account'].format(**self.params, user=user, password=password), print_only=self.params['print_only'])
        output = result_set.fetchall()
        if not self.params['print_only'] and len(output) > 0:
            (account_details,) = output[0]
            account_name = json.loads(account_details)['accountName']
            url = json.loads(account_details)['loginUrl']
        return account_name, url

    def run(self):
        db_type=None
        v = self.params
        print_only = v['print_only']

        # DB Types
        db_types = ['PRIMARY', 'FLASH']
    
        # Using ACCOUNTADMIN role
        self.execute('Use role ACCOUNTADMIN', print_only=False)

        # Setup Reader Account
        if not self.reader_account_details['account_name']:

            # Using Configuration database    
            self.execute(f"Use database {v['config_db']}", print_only=False)

            # Creating Reader Account
            logger.info("Creating Reader Account")
            account_name = f"EXT_ACC_CLIENT_ID_{v['ext_client_id']}"
            user = f"EXT_ADMIN_CLIENT_ID_{v['ext_client_id']}" if not self.reader_account_details['admin_user'] else self.reader_account_details['admin_user']
            result_set = self.create_reader_account(user=user, password=self.reader_account_details['admin_password'])
            account, url = result_set
            self.reader_account_details['account'] = account
            self.reader_account_details['account_name'] = account_name
            self.reader_account_details['url'] = url
            self.reader_account_details['admin_user'] = user
            self.reader_account_details['login_account'] = url.split('//')[1].split('.snowflakecomputing.com')[0] if url else None
            logger.info(f"Reader Account details: {self.reader_account_details}")

            logger.info("Adding Reader Account details to the External Client ID in the Mapping table")
            self.execute(self.common['sql_update_raccount_mapping_table'].format(**v, **self.reader_account_details), print_only=print_only)

        else:
            logger.info(f"...Skipping Reader Account Creation. Reader Account {self.reader_account_details['account_name']} already exist.")
            result_set = self.execute(self.common['sql_show_managed_account'].format(**v, account=self.reader_account_details['account_name']), print_only=False)
            output = result_set.fetchall()
            if len(output) > 0:
                account_details = output[0]
                self.reader_account_details['account'] = account_details[3]
                self.reader_account_details['url'] = account_details[5]
                self.reader_account_details['login_account'] = account_details[5].split('//')[1].split('.snowflakecomputing.com')[0] if account_details[5] else None
                self.reader_account_details['admin_user'] = self.reader_account_details['admin_user']
                self.reader_account_details['admin_password'] = self.reader_account_details['admin_password']
                logger.info(f"Reader Account details: {self.reader_account_details}")
                
        if self.reader_account_details.get('login_account') is None:
            raise RuntimeError("Failed while creating or fetching the Reader Account details")

        # Share
        logger.info("Creating DB Share")
        self.execute(f"Use database {v['config_db']}", print_only=False)
        self.execute(self.common['sql_create_share'].format(**v), print_only=print_only)

        ## Setup Primary/Flash DB
        for db_type in db_types:
            filter_column = 'context_id' if db_type == "PRIMARY" else 'event_owner_id'
            if v[filter_column]:
                db = f'{db_type.lower()}_db'
                schema = f'{db_type.lower()}_schema'
                ignore_tables = f'{db_type.lower()}_ignore_tables'

                logger.info(f"Setting up {db_type} Database")
                self.execute(f"Use database {v[db]}", print_only=False)

                # Creating VIEWS and Granting them to DB Role
                count = 0
                for table_name in self.execute(self.common['sql_get_tables'].format(**v, db_schema=v[schema], ignore_tables=v[ignore_tables]), print_only=False):
                    # Views
                    view_name = f"v_EXT_{table_name[0]}"
                    # print(view_name)
                    result_set = self.execute(self.common['sql_get_view'].format(**v, db_name=v[db], db_schema=v[schema], view_name=view_name), print_only=False)
                    # print(result_set)
                    if len(result_set.fetchall()) == 0:
                        logger.info(f"Creating View.. {view_name}")
                        self.execute(self.common['sql_create_view'].format(**v, db_name=v[db], db_schema=v[schema], table_name=table_name[0], view_name=view_name, filter_column=filter_column), print_only=print_only)
                        count += 1
                    else:
                        logger.info(f"View {view_name} already exists")

                # Granting Primary DB & Schema to DB Role 
                if count >= 0:
                    # DB Roles
                    logger.info("Creating DB Roles")
                    self.execute(self.common['sql_create_db_role'].format(**v, db_name=v[db], db_type=db_type), print_only=print_only)
                    
                    logger.info(f"Granting {db_type} DB, Schema & Views to the DB Role")
                    self.execute(self.common['sql_grant_db_to_db_role'].format(**v, db_name=v[db], db_type=db_type), print_only=self.params['print_only'])
                    self.execute(self.common['sql_grant_schema_to_db_role'].format(**v, db_name=v[db], db_schema=v[schema], db_type=db_type), print_only=self.params['print_only'])
                    self.execute(self.common['sql_grant_view_to_db_role'].format(**v, view_name=view_name, db_name=v[db], db_schema=v[schema], db_type=db_type), print_only=self.params['print_only'])

                    logger.info(f"Granting {db_type} DB views to the ENGINEER Role")
                    self.execute(self.common['sql_grant_view'].format(**v, db_name=v[db], db_schema=v[schema])) # ENGINEER role should have SELECT permission on VIEWS for debugging

                    logger.info(f"Granting {db_type} DB, CONFIG DB, DB_Role access to the Share")           
                    self.execute(self.common['sql_grant_db_to_share'].format(**v, db_name=v[db]), print_only=self.params['print_only'])
                    self.execute(self.common['sql_grant_reference_usage_to_share'].format(**v), print_only=self.params['print_only'])
                    self.execute(self.common['sql_grant_db_role_to_share'].format(**v, db_name=v[db], db_type=db_type), print_only=print_only)

                    # Update Share and Mapping Table with Reader Account Details
                    logger.info("Associating DB Share with the Reader Account")
                    self.execute(self.common['sql_alter_share'].format(**v, **self.reader_account_details), print_only=print_only)

                    logger.info(f"Setup of Primary Database {v[db]} for external client {v['ext_client_name']} is done. Reader Account Details are: {self.reader_account_details}")
                else:
                    logger.error(f"Either VIEWS already exist or no tables found. Note: Account Admin should have SELECT privileges on all the tables in schema {v[db]}.{v[schema]}")
        
        return self.reader_account_details