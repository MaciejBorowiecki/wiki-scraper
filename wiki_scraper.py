import argparse
from wiki_manager import WikiManager


def validate_arguments(parser: argparse.ArgumentParser, args):
    """
    Validates the correctness of the given arguments, sets error in the parser
    in case of incorrect arguments. 
    """

    def _check_mutually_dependent(*args) -> bool:
        """
        Returns True when either all or none arguments are provided, False otherwise.
        """
        count_present = sum(1 for arg in args if arg is not None and arg is not False)
        return count_present == 0 or count_present == len(args)
    
    # Check whether any of the main modes arguments were given.
    modes = [
        args.summary,
        args.table,
        args.count_words,
        args.analyze_relative_word_frequency,
        args.auto_count_words
    ]

    if not any(modes):
        parser.error("None of the main modes selected.")

    if not _check_mutually_dependent(args.table, args.number):
        parser.error(
            "Arguments '--table' and '--number' must be used together.")

    if args.first_row_is_header and (args.table == None or args.number == None):
        parser.error(
            "Arguments '--table' and '--number' are required for '--first-row-is-header'.")

    if args.number and args.number <= 0:
        parser.error("Argument '--number' needs to be greater or equal to 1")

    if not _check_mutually_dependent(args.analyze_relative_word_frequency, args.mode, args.count):
        parser.error(
            "Arguments '--analyze-relative-word-frequency', '--count' and '--mode' must be used together.")
        
    if args.mode and args.mode != 'article' and args.mode != 'language':
        parser.error("The only valid modes are 'article' and 'language'.")

    if args.analyze_relative_word_frequency == None and args.chart:
        parser.error(
            "Arguments '--analyze-relative-word-frequency', '--count' and '--mode' must be used " + 
            "in order to use '--chart'."
        )
    
    if not _check_mutually_dependent(args.auto_count_words, args.depth, args.wait):
        parser.error("Arguents '--auto-count-words', '--depth' and '--wait' must be used together.")
    
    if args.depth and args.depth < 0:
        parser.error("Depth for crawling must be greater or equal to 0.")
        
    if args.wait and args.wait < 0:
        parser.error("Waiting time for crawling msut be greater or equal to 0.")
    

def parse_arguments():
    parser = argparse.ArgumentParser()

    # summary extraction arguments
    summary_group = parser.add_argument_group('Summary Extraction')
    summary_group.add_argument(
        '--summary',
        type=str,
        metavar='PHRASE',
        help='Fetch and print the first paragraph of the wiki article for the given PHRASE.'

    )

    # table extractoin arguments
    table_group = parser.add_argument_group('Table Extraction')
    table_group.add_argument(
        '--table',
        type=str,
        metavar='PHRASE',
        help='Fetch and display a specific table from the article found for PHRASE.'
    )
    table_group.add_argument(
        '--number',
        type=int,
        metavar='INDEX',
        help='Index of the table to fetch (1-based). Required if --table is used.'
    )
    table_group.add_argument(
        '--first-row-is-header',
        action='store_true',
        help='Use the first row of the table as the header.'
    )

    # word occurences and statistics arguments
    statistics_group = parser.add_argument_group('Article Content Statistics')
    statistics_group.add_argument(
        '--count-words',
        type=str,
        metavar='PHRASE',
        help='Count the occurrences of words from the article found for PHRASE. Save results to JSON.'
    )
    statistics_group.add_argument(
        '--analyze-relative-word-frequency',
        action='store_true',
        help=(
            'Analyze the frequency of wiki words (collected at `count-words`) ' +
            'in relation to the frequency of these words in the wiki language.'
        )
    )
    statistics_group.add_argument(
        '--mode',
        type=str,
        metavar='MODE',
        help=(
            'Sort by frequency of words in ARTICLE or sort by LANGUAGE of the wiki. ' +
            'Required if --analyze-relative-word-frequency is used.'
        )
    )
    statistics_group.add_argument(
        '--count',
        type=int,
        metavar='ROWS',
        help=(
            'Number of words to compare their frequency between the wiki articles and the wiki language ' +
            'Required if --analyze-relative-word-frequency is used.'
        )
    )
    statistics_group.add_argument(
        '--chart',
        type=str,
        metavar='PATH',
        help='Create a chart comparing COUNT words of wiki and wiki language frequency.'
    )
    statistics_group.add_argument(
        '--auto-count-words',
        type=str,
        metavar='PHRASE',
        help='Start automatic word counting beginning at PHRASE and following internal links.'
    )
    statistics_group.add_argument(
        '--depth',
        type=int,
        metavar='DEPTH',
        help='Maximum link distance from the start phrase to traverse (0 = only start phrase).'
    )
    statistics_group.add_argument(
        '--wait',
        type=float,
        metavar='TIME',
        help='Interval in seconds between processing articles.'
    )

    args = parser.parse_args()
    validate_arguments(parser, args)

    return args


def main():
    args = parse_arguments()
    manager = WikiManager(args)
    manager.handle_args()


if __name__ == '__main__':
    main()
