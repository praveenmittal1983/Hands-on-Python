from logger_setup import LoggerSetup
from snowflake_connector import SnowflakeConnector

logger = LoggerSetup.get_logger()

class MappingTable(SnowflakeConnector):
    def __init__(self, locale, cleanup=False, print_only=True) -> None:
        logger.info("Module: Setting up Mapping Table")
        super().__init__(locale, print_only=print_only)
        self.client_details = {}
        self.cleanup = cleanup

    def validate_mapping_table(self):
        create_flag = False
        insert_flag = False
        output = None
        try:
            output = self.execute(self.common['sql_distinct_external_client_id'].format(**self.params), print_only=False)
        except RuntimeError as e_msg:
            create_flag = True
            insert_flag = True
            logger.error(f"Validation results: {e_msg}")

        # Check if record already exist
        if output:
            (count,) = output.fetchone()
            if count > 1:
                raise RuntimeError(f"External clients: {self.params['ext_client_name']} has multiple ID in the Mapping Table")
            if count == 0:
                insert_flag = True

        # In Cleanup mode, it should not update the table
        if self.cleanup and (create_flag or insert_flag):
            raise RuntimeError(f"Script in cleanup mode trying to Create or Insert record in the Mapping Table")
        
        return create_flag, insert_flag

    def create_or_insert_mapping_table(self):
        create_flag, insert_flag = self.validate_mapping_table()
        
        # Creating the mapping table
        if create_flag:
            logger.info("Creating Mapping Table")
            self.execute(self.common['sql_create_mapping_table'].format(**self.params), print_only=self.params['print_only'])

        # Insert the record
        if insert_flag:
            self.execute(self.common['sql_insert_mapping_table'].format(**self.params), print_only=self.params['print_only'])
        
        # Get Client ID
        output = self.execute(self.common['sql_get_external_client_id'].format(**self.params), print_only=False)
        if output:
            (client_id, reader_account_name, reader_account_id) = output.fetchone()
            self.client_details['ext_client_id'] = client_id
            self.client_details['reader_account_name'] = reader_account_name
            self.client_details['reader_account_id'] = reader_account_id
            self.params['ext_client_id'] = client_id

        # Updating Context ID and Event Owner ID in the Mapping table
        if not self.cleanup:
            logger.info(f"Updating ContextIDs: ({self.params['context_id']}) and EventOwnerIDs: ({self.params['event_owner_id']}) in the Mapping Table")
            try:
                output = self.execute(self.common['sql_update_mapping_table'].format(**self.params), print_only=self.params['print_only'])
            except RuntimeError as e_msg:
                logger.error(f"Validation results: {e_msg}")

    def run(self):
        # Setup Mapping table
        self.execute('Use role ACCOUNTADMIN', print_only=False)
        self.create_or_insert_mapping_table()
        logger.info(f"Mapping table setup for client {self.params['ext_client_name']} completed. Details: {{Client_ID: {self.client_details['ext_client_id']}, Client_Name: {self.params['ext_client_name']}, Reader_Account_Name: {self.client_details['reader_account_name']}}}")

        return self.client_details