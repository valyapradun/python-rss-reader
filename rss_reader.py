import argparse
from src.rss_class import RssReader


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument("source",
                        help="RSS URL",
                        type=str)

    parser.add_argument("--version",
                        action="version",
                        version="Version 1.1",
                        help="Print version info")

    parser.add_argument("--json",
                        help="Print result as JSON in stdout",
                        action="store_true")

    parser.add_argument("--verbose",
                        help="Outputs verbose status messages",
                        action="store_true")

    parser.add_argument("--limit",
                        help="Limit news topics if this parameter provided",
                        type=int)

    args = parser.parse_args()
    rss_source = args.source
    limit = args.limit
    json = args.json
    verbose = args.verbose

    rss = RssReader(rss_source, limit, json, verbose)
    rss.print_rss()


if __name__ == "__main__":
    main()
