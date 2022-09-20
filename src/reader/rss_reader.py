from reader.rss_utils import parse_argument
from reader.rss_entities import RssReader


def main():
    """
    Main method for rss_reader.

    Procedure:
    - getting command line arguments
    - creating an object of class RssReader
    - checking 'limit' parameter
    - parsing of rss
    - displaying the result on the screen
    """
    args = parse_argument()
    (rss_source, limit, json, verbose) = (args.source, args.limit, args.json, args.verbose)

    rss = RssReader(rss_source, limit, json, verbose)
    rss.check_limit()
    rss_json = rss.parse_rss()
    if rss_json is not None:
        rss.print_rss(rss_json)


if __name__ == "__main__":
    main()

