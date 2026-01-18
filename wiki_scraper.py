import argparse
from wiki_manager import WikiManager


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--summary',
        type=str,
        metavar='PHRASE',
        help='Fetch and print the first paragraph of the wiki article for the given phrase.'

    )

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    manager = WikiManager(args)
    manager.handle_args()


if __name__ == '__main__':
    main()
