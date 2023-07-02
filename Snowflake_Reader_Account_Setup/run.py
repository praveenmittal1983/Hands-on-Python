import argparse
from cleanup_account import CleanUpAcount
from provider_account import SetupProviderAcount
from consumer_account import SetupConsumerAcount
from logger_setup import LoggerSetup

logger = LoggerSetup.get_logger()

def processArgs():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--locale', default='eu')
    parser.add_argument('--reader_admin_credentials', default='Admin@123!')
    parser.add_argument('--reader_user_credentials', default='User@123!')
    parser.add_argument('--print_only', default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('--cleanup', default=False, action=argparse.BooleanOptionalAction)
    return parser.parse_args()

if __name__ == "__main__":
    args = processArgs()
    print(f"Running program with arguments {args}")
    locale = args.locale.upper()
    try:
        if args.cleanup:
            CleanUpAcount(locale=locale, print_only=args.print_only).run()
        else:
            reader_account = SetupProviderAcount(
                locale=locale, reader_admin_credentials=args.reader_admin_credentials, print_only=args.print_only).run()

            if reader_account['account']:
                SetupConsumerAcount(
                    locale=locale, reader_account=reader_account, reader_user_credentials=args.reader_user_credentials, print_only=args.print_only).run()
            else:
                logger.error(f"Could not setup Consumer Account. Invalid account {reader_account}")

    except RuntimeError as e:
        logger.error(f"Msg: {e}")