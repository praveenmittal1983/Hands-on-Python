import argparse, logging
from src.wordcount import WordCount

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# processing arguments
def processArgs():
    parser = argparse.ArgumentParser(add_help=True, description="Word Count Program")
    parser.add_argument('-f', '--filepath', help='provide complete file path', required=True)
    return parser.parse_args()

if __name__=="__main__":
    args = processArgs()
    logger.info(f"Starting program with arguments {args}")

    try:
        wc = WordCount(args.filepath)
        if wc.validate_filepath():
            wc.word_count()
            wc.print_results()
        else:
            logger.error("Invalid filepath")
    except RuntimeError as e:
        logger.error(f"Program failed to run: {e}")