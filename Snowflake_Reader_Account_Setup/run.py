import argparse
from mapping_table import MappingTable
from cleanup_account import CleanUpAcount
from provider_account import SetupProviderAcount
from consumer_account import SetupConsumerAcount
from logger_setup import LoggerSetup

logger = LoggerSetup.get_logger()


def processArgs():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--locale', default='eu')
    parser.add_argument('--reader_admin', default='ReaderAdmin')
    parser.add_argument('--reader_user', default='ReaderUser')
    parser.add_argument('--reader_admin_credentials', default='Admin@123!')
    parser.add_argument('--reader_user_credentials', default='User@123!')
    parser.add_argument('--print_only', default=True,
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--cleanup', default=False,
                        action=argparse.BooleanOptionalAction)
    return parser.parse_args()


if __name__ == "__main__":
    args = processArgs()
    logger.info(f"Starting program with arguments {args}")
    locale = args.locale.upper()
    try:
        client_details = MappingTable(locale=locale, cleanup=args.cleanup, print_only=args.print_only).run()
        if args.cleanup:
            CleanUpAcount(locale=locale, client_details = client_details, print_only=args.print_only).run()
        else:
            reader_account = SetupProviderAcount(
                locale=locale, reader_admin=args.reader_admin, reader_admin_credentials=args.reader_admin_credentials, client_details = client_details, print_only=args.print_only).run()

            if reader_account['account'] and reader_account['admin_user']:
                SetupConsumerAcount(
                    locale=locale, reader_account=reader_account, reader_user=args.reader_user, reader_user_credentials=args.reader_user_credentials, client_details = client_details, print_only=args.print_only).run()
            else:
                logger.error(f"Could not setup Consumer Account. Invalid account or missing user. Details: {reader_account}")

    except RuntimeError as e:
        logger.error(f"Msg: {e}")
