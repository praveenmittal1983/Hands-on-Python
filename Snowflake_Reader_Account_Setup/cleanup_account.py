from logger_setup import LoggerSetup
from snowflake_connector import SnowflakeConnector

logger = LoggerSetup.get_logger()

class CleanUpAcount(SnowflakeConnector):
    def __init__(self, locale, print_only=True) -> None:
        logger.info("Module: Cleanup")
        super().__init__(locale, print_only=print_only)

    def run(self):
        v = self.params
        print_only = v['print_only']

        # Provider Account
        self.execute('Use role ACCOUNTADMIN', print_only=False)
        self.execute(f"Use database {v['db_name']}", print_only=False)

        self.execute(self.config['sql_del_access_table'].format(**v), print_only=print_only)
        self.execute(self.config['sql_del_db_role'].format(**v), print_only=print_only)
        self.execute(self.config['sql_del_share'].format(**v), print_only=print_only)
        self.execute(self.config['sql_del_reader_account'].format(**v), print_only=print_only)

        # We dont need to clean up reader account, as once account is deleted, all the objects are gone
        logger.info(f"Clean-up process for Context Id {v['context_id']} completed")
        return