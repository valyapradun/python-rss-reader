import feedparser
import unicodedata
import dateutil.parser as parser
import pandas as pd
import json
from os import path
import sys
from reader.rss_utils import get_logger, log_decorator, exceptions_suppressing_decorator
from reader.rss_exeptions import RssReaderCacheException

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

__JSON_FILE__ = "data/news.json"


class RssReader:
    """
        A class to represent a rss object.

        Attributes
        ----------
        rss_source : str
             RSS URL
        limit : int
             Limit news topics
        json: bool
             Print result as JSON in stdout
        verbose: bool
             Outputs verbose status messages
        date: int
             Date for reading cached news

        Methods
        -------
        check_limit(self):
            Checking the entered parameter '--limit' and feed size.
        parse_rss(self):
            Parse rss and return a dictionary with its contents
        print_rss(self, rss_json):
            Print output to console in human readable format or as json
        write_json(self, rss_json):
            Write rss-news in json file
        read_cashed_news(self):
            Read json file and filter records by date and source

        """

    def __init__(self, rss_source, limit=None, json=True, verbose=True, date=None):
        """
        The initialization method for the RssReader instance.
        :param str rss_source: RSS URL
        :param int limit: Limit news topics
        :param json: Print result as JSON in stdout
        :param verbose: Outputs verbose status messages
        """
        self.rss_source = rss_source
        self.limit = limit
        if rss_source is not None:
            self.news_feed = feedparser.parse(rss_source)
            self.number_news = len(self.news_feed.entries)
            if limit is None:
                self.limit = self.number_news
            else:
                self.limit = limit
        self.verbose = verbose
        self.json = json
        self.logger_obj = get_logger(self.verbose)
        self.date = date

    @log_decorator()
    def check_limit(self) -> int:
        """
        Checking the entered parameter '--limit' and feed size.
        If `--limit` is larger than feed size then user should get _all_ available news.
        :return: self.limit
        """
        if self.limit > self.number_news:
            self.limit = self.number_news
        return self.limit

    @exceptions_suppressing_decorator
    @log_decorator
    def parse_rss(self) -> dict:
        """
        Parse rss and return a dictionary with its contents
        :return: dictionary with rss contents
        """
        rss_json = {}
        entries = []

        for entry in self.news_feed.entries[0:self.limit]:
            keys_entry = entry.keys()
            entry_json = {"rss_source": self.rss_source,
                          "feed": unicodedata.normalize("NFKC", self.news_feed.feed.title)}

            if "title" in keys_entry:
                entry_json["title"] = entry.title

            if "published" in keys_entry:
                entry_json["date"] = str(parser.parse(entry.published))

            if "link" in keys_entry:
                # entry_json["link"] = unicodedata.normalize("NFKC", entry.link)
                entry_json["link"] = entry.link

            if "summary" in keys_entry:
                # entry_json["summary"] = unicodedata.normalize("NFKC", entry.summary)
                entry_json["summary"] = entry.summary

            links = []
            if "links" in keys_entry:
                for link in entry.links:
                    link_json = {"index": entry.links.index(link) + 1, "href": link.href, "type": link.type}
                    links.append(link_json)
            entry_json["links"] = links
            entries.append(entry_json)

        rss_json["entries"] = entries

        return rss_json

    @exceptions_suppressing_decorator
    @log_decorator
    def print_rss(self, rss_json):
        """
        Print output to console in human readable format or as json
        :param rss_json: dictionary with rss contents
        """
        if self.json:
            print(rss_json)
        else:
            for entry in rss_json['entries']:
                print('\n----------------------\n')
                links_attribute = "links"
                main_attributes = [*filter(lambda i: i != links_attribute, entry.keys())]
                for key in main_attributes:
                    print(f"{key.capitalize()}: {entry[key]}")
                if links_attribute in entry.keys():
                    print("\nLinks:")
                    for link in entry["links"]:
                        print(f"[{entry['links'].index(link) + 1}]: {link['href']} ({link['type']})")

    @exceptions_suppressing_decorator
    @log_decorator
    def write_json(self, rss_json):
        """
        Write rss-news in json file
        :param rss_json: dictionary with rss contents
        """
        filename = __JSON_FILE__
        if path.isfile(filename) is False:
            file_data = {"data": [rss_json]}
            with open(filename, "w", encoding="utf-8") as outfile:
                json.dump(file_data, outfile, ensure_ascii=False)
        else:
            with open(filename, "r+", encoding="utf-8") as outfile:
                file_data = json.load(outfile)
                file_data["data"].append(rss_json)
                outfile.seek(0)
                json.dump(file_data, outfile, ensure_ascii=False)

    @exceptions_suppressing_decorator
    @log_decorator
    def read_cashed_news(self):
        """
        Read json file and filter records by date and source
        """
        filename = __JSON_FILE__
        if path.isfile(filename) is False:
            raise RssReaderCacheException(f"\nThe cache does not exist. Please read some news first.")
        else:
            df = pd.read_json(filename, orient="split")

            exploded_df = df.explode("entries").drop_duplicates()
            exploded_df = pd.DataFrame(exploded_df['entries'].tolist())
            exploded_df['formatted_date'] = exploded_df['date'].str.slice(0, 10).str.replace("-", "")

            filtered_by_date_df = exploded_df[exploded_df['formatted_date'] == str(self.date)]
            filtered_by_date_df = filtered_by_date_df.drop(columns=["formatted_date"])

            if self.rss_source is None:
                entries = filtered_by_date_df.to_dict('records')

                if self.limit is None:
                    self.limit = len(entries)

                if self.limit <= len(entries):
                    return entries[:self.limit]
                else:
                    return entries
            else:
                filtered_by_source_df = filtered_by_date_df[filtered_by_date_df['rss_source'] == self.rss_source]
                entries = filtered_by_source_df.to_dict('records')
                if (self.limit is not None) & (self.limit <= len(entries)):
                    return entries[:self.limit]
                else:
                    return entries
