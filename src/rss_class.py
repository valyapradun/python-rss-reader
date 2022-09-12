import feedparser
from src.utils import exceptions_suppressing_decorator


class RssReader:

    def __init__(self, rss_source, limit=None, json=None, verbose=None):
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
        '''

        :return:
        '''
        # if self.limit > self.number_news:
        #    self.limit = self.number_news
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
