import feedparser
import json
from src.utils import exceptions_suppressing_decorator


class RssReader:

    def __init__(self, rss_source, limit=None, json=True, verbose=True):
        """
        The initialization method for the RssReader instance.
        :param str rss_source: RSS URL
        :param int limit: Limit news topics
        :param json: Print result as JSON in stdout
        :param verbose: Outputs verbose status messages
        """
        self.rss_source = rss_source
        self.json = json
        self.verbose = verbose
        self.news_feed = feedparser.parse(rss_source)
        self.number_news = len(self.news_feed.entries)
        if limit is None:
            self.limit = self.number_news
        else:
            self.limit = limit

    def check_limit(self):
        """
        Checking the entered parameter '--limit' and feed size.
        If `--limit` is larger than feed size then user should get _all_ available news.
        :return: self.limit
        """
        if self.limit > self.number_news:
            self.limit = self.number_news

    @exceptions_suppressing_decorator
    def read_news(self):

        self.check_limit()

        print(f"\nFeed: {self.news_feed.feed.title}")

        for entry in self.news_feed.entries[0:self.limit]:
            keys_entry = entry.keys()

            print('\n----------------------')
            if 'title' in keys_entry:
                print(f"\nTitle: {entry.title}")
            if 'published' in keys_entry:
                print(f"Date: {entry.published}")
            if 'link' in keys_entry:
                print(f"Link: {entry.link}")
            if 'summary' in keys_entry:
                print(f"\n{entry.summary}")

            if 'links' in keys_entry:
                print("\nLinks:")
                for link in entry.links:
                    print(f"[{entry.links.index(link) + 1}]: {link.href} ({link.type})")

    @exceptions_suppressing_decorator
    def parse_rss(self):
        self.check_limit()
        rss_dictionary = {"feed": self.news_feed.feed.title}
        entries = []

        for entry in self.news_feed.entries[0:self.limit]:
            keys_entry = entry.keys()
            entry_dictionary = {}

            if "title" in keys_entry:
                entry_dictionary["title"] = entry.title

            if "published" in keys_entry:
                entry_dictionary["date"] = entry.published

            if "link" in keys_entry:
                entry_dictionary["link"] = entry.link

            if "summary" in keys_entry:
                entry_dictionary["summary"] = entry.summary

            links = []
            if "links" in keys_entry:
                for link in entry.links:
                    link_dictionary = {"index": entry.links.index(link) + 1, "href": link.href, "type": link.type}
                    links.append(link_dictionary)
            entry_dictionary["links"] = links
            entries.append(entry_dictionary)

        rss_dictionary["entries"] = entries

        return rss_dictionary

    def print_rss(self):
        rss_json = self.parse_rss()
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
