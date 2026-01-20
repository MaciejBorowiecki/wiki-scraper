import argparse
from wiki_manager import WikiManager


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

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    manager = WikiManager(args)
    manager.handle_args()


if __name__ == '__main__':
    main()
