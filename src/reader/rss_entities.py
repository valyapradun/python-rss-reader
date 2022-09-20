import feedparser
import unicodedata
from reader.rss_utils import get_logger, log_decorator, exceptions_suppressing_decorator


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

        Methods
        -------
        check_limit(self):
            Checking the entered parameter '--limit' and feed size.
        parse_rss(self):
            Parse rss and return a dictionary with its contents
        print_rss(self, rss_json):
            Print output to console in human readable format or as json
        """

    def __init__(self, rss_source, limit=None, json=True, verbose=True):
        """
        The initialization method for the RssReader instance.
        :param str rss_source: RSS URL
        :param int limit: Limit news topics
        :param json: Print result as JSON in stdout
        :param verbose: Outputs verbose status messages
        """
        self.rss_source = rss_source
        self.verbose = verbose
        self.json = json
        self.news_feed = feedparser.parse(rss_source)
        self.number_news = len(self.news_feed.entries)
        if limit is None:
            self.limit = self.number_news
        else:
            self.limit = limit
        self.logger_obj = get_logger(self.verbose)

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
        rss_json = {"feed": unicodedata.normalize("NFKC", self.news_feed.feed.title)}
        entries = []

        for entry in self.news_feed.entries[0:self.limit]:
            keys_entry = entry.keys()
            entry_json = {}

            if "title" in keys_entry:
                entry_json["title"] = unicodedata.normalize("NFKC", entry.title)

            if "published" in keys_entry:
                entry_json["date"] = entry.published

            if "link" in keys_entry:
                entry_json["link"] = unicodedata.normalize("NFKC", entry.link)

            if "summary" in keys_entry:
                entry_json["summary"] = unicodedata.normalize("NFKC", entry.summary)

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
            print(f"\nFeed: {rss_json['feed']}")
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