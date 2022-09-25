import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

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
    (rss_source, limit, json, verbose, date) = (args.source, args.limit, args.json, args.verbose, args.date)

    if isinstance(rss_source, list):
        rss_source = rss_source[0]

    if date is None:
        rss = RssReader(rss_source, limit, json, verbose, date)
        rss.check_limit()
        rss_json = rss.parse_rss()
        if rss_json is not None:
            rss.write_json(rss_json)
            rss.print_rss(rss_json)
    else:
        rss = RssReader(rss_source, limit, json, verbose, date)
        entries = rss.read_cashed_news()
        if len(entries) != 0:
            rss_json = {"entries": entries}
            rss.print_rss(rss_json)
        else:
            print(f"Error: no news for specified source ({rss_source}) or date ({date}).")


if __name__ == "__main__":
    main()
