import json
from logger_setup import LoggerSetup
from snowflake_connector import SnowflakeConnector

logger = LoggerSetup.get_logger()

class SetupProviderAcount(SnowflakeConnector):
    def __init__(self, locale, reader_admin_credentials, print_only=True) -> None:
        logger.info("Module: Setup Provider Account")
        super().__init__(locale, print_only=print_only)
        self.reader_account_details = {}
        self.reader_account_details['admin_password'] = reader_admin_credentials
    
    def validate_mapping_table(self):
        create_flag = False
        output = None
        try:
            output = self.execute(self.config['sql_validate_mapping_table'].format(**self.params), print_only=False)
        except RuntimeError as e_msg:
            create_flag = True
            logger.error(f"Validation results: {e_msg}")

        # Check if record already exist
        if output:
            (count,) = output.fetchone()
            if count > 0:
                raise RuntimeError(f"Data already exist in {self.params['db_name']}.{self.params['schema']}.EXT_MAPPING_TABLE for context {self.params['context_id']}")
                
        return create_flag

    def create_or_insert_mapping_table(self):
        create_flag = self.validate_mapping_table()
        
        # Creating the mapping table
        if create_flag:
            logger.info("Creating Mapping Table")
            self.execute(self.config['sql_create_mapping_table'].format(**self.params), print_only=self.params['print_only'])

        # Insert the record
        self.execute(self.config['sql_insert_mapping_table'].format(**self.params), print_only=self.params['print_only'])
        
    def grant_db_roles(self, db_flag=False, schema_flag=False, view_name=None):
        if db_flag:
            self.execute(self.config['sql_grant_db_to_db_role'].format(**self.params), print_only=self.params['print_only'])
        if schema_flag:
            self.execute(self.config['sql_grant_schema_to_db_role'].format(**self.params), print_only=self.params['print_only'])
        if view_name:
            self.execute(self.config['sql_grant_view_to_db_role'].format(**self.params, view_name=view_name), print_only=self.params['print_only'])

    def grant_share(self):
        self.execute(self.config['sql_grant_db_to_share'].format(**self.params), print_only=self.params['print_only'])
        self.execute(self.config['sql_grant_db_role_to_share'].format(**self.params), print_only=self.params['print_only'])

    def create_reader_account(self, user, password):
        account_name = None
        url = None
        result_set = self.execute(self.config['sql_create_managed_account'].format(**self.params, user=user, password=password), print_only=self.params['print_only'])
        if not self.params['print_only']:
            (account_details,) = result_set.fetchall()[0]
            account_name = json.loads(account_details)['accountName']
            url = json.loads(account_details)['loginUrl']
        return account_name, url

    def run(self):
        count = 0
        v = self.params
        print_only = v['print_only']

        self.execute('Use role ACCOUNTADMIN', print_only=False)
        self.execute(f"Use database {v['db_name']}", print_only=False)

        ## Setup Provider Account
        for table_name in self.execute(self.config['sql_get_tables'].format(**v), print_only=False):
            # Ignore Mapping table
            if table_name[0].startswith('EXT_'):
                continue

            if count == 0:
                logger.info("Updating Mapping table")
                self.create_or_insert_mapping_table()

                # DB Roles
                logger.info("Creating DB Roles")
                self.execute(self.config['sql_create_db_role'].format(**v), print_only=print_only)
                self.grant_db_roles(db_flag=True, schema_flag=True)

                # Share
                logger.info("Creating DB Share")
                self.execute(self.config['sql_create_share'].format(**v), print_only=print_only)
                self.grant_share()

                # Reader Account
                logger.info("Creating Reader Account")
                user = f"ACC_CONTEXT_ID_{v['context_id']}"
                result_set = self.create_reader_account(user=user, password=self.reader_account_details['admin_password'])
                account, url = result_set
                self.reader_account_details['account'] = account
                self.reader_account_details['url'] = url
                self.reader_account_details['admin_user'] = user
                self.reader_account_details['login_account'] = url.split('//')[1].split('.snowflakecomputing.com')[0] if url else None
                # logger.info(f"Reader Account details: {self.reader_account_details}")

                self.execute(self.config['sql_alter_share'].format(**v, **self.reader_account_details), print_only=print_only)
                self.execute(self.config['sql_update_mapping_table'].format(**v, **self.reader_account_details), print_only=print_only)

            # Views
            logger.info("Creating View")
            view_name = f"v_EXT_{v['context_id']}_{table_name[0]}"
            self.execute(self.config['sql_create_view'].format(**v, table_name=table_name[0], view_name=view_name), print_only=print_only)
            self.grant_db_roles(db_flag=False, schema_flag=False, view_name=view_name)
            count += 1

        if count == 0:
            logger.error(f"No tables found. Note: Account Admin should have SELECT privileges on all the tables in schema {v['db_name']}.{v['schema']}")
        else:
            logger.info("Updating Views access")
            self.execute(self.config['sql_grant_view'].format(**v)) # ENGINEER role should have SELECT permission on VIEWS for debugging
            logger.info(f"Setup of Provider Account for Context Id {v['context_id']} completed. Details: {self.reader_account_details}")
            return self.reader_account_details