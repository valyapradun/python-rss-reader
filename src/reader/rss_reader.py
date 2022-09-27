import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from reader.rss_utils import parse_argument, pass_to_html, pass_to_pdf
from reader.rss_entities import RssReader


def main():
    """
    Main method for rss_reader.

    Procedure:
    - getting command line arguments
    - if date argument is None (means without reading cached news):
          -- creating an object of class RssReader
          -- checking 'limit' parameter
          -- parsing of rss
          -- caching news to local file
          -- displaying the result on the screen
    - if date argument is not None (means with reading cached news):
          -- creating an object of class RssReader
          -- reading cached news
          -- displaying the result on the screen
    - if html_path argument is not None:
          -- writing news to html file
    - if pdf_path argument is not None:
          -- writing news to pdf file
    """
    args = parse_argument()
    rss_source = args.source
    if isinstance(rss_source, list):
        rss_source = rss_source[0]
    limit = args.limit
    json = args.json
    verbose = args.verbose
    date = args.date
    html_path = args.to_html
    pdf_path = args.to_pdf

    rss_json = {}

    if date is None:
        rss = RssReader(rss_source, limit, json, verbose, date)
        rss.check_limit()
        rss_json = rss.parse_rss()
        if rss_json is not None:
            rss.write_json(rss_json)
            rss.print_rss(rss_json)
    else:
        rss = RssReader(rss_source, limit, json, verbose, date)
        rss.check_date()
        entries = rss.read_cashed_news()

        if entries is None:
            print(f"Error: no news for specified source ({rss_source}) or date ({date}).")
        elif len(entries) != 0:
            rss_json = {"entries": entries}
            rss.print_rss(rss_json)
        else:
            print(f"Error: no news for specified source ({rss_source}) or date ({date}).")

    if html_path is not None:
        pass_to_html(html_path, rss_json)

    if pdf_path is not None:
        pass_to_pdf(pdf_path, rss_json)


if __name__ == "__main__":
    main()
