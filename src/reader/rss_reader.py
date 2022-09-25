from reader.rss_utils import parse_argument
from reader.rss_entities import RssReader
import pandas as pd


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
    (rss_source, limit, json, verbose, published_date) = (args.source, args.limit, args.json, args.verbose, args.date)

    if isinstance(rss_source, list):
        rss_source = rss_source[0]

    print(rss_source)

    if published_date is None:
        rss = RssReader(rss_source, limit, json, verbose)
        rss.check_limit()
        rss_json = rss.parse_rss()
        if rss_json is not None:
            rss.write_json(rss_json)
            rss.print_rss(rss_json)
    else:
        df = pd.read_json("data/news.json", orient="split")
        df1 = df.explode("entries")
        df1 = pd.DataFrame(df1['entries'].tolist())
        print(df1.columns)
        #df1 = df1.filter()
        #"date": "2022-09-25 14:13:00+03:00"
        df2 = df1[df1['date'] == published_date]
        #df1["title"] = df1["entries(title)"]


        print(df2)




if __name__ == "__main__":
    main()

