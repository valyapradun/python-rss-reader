import unittest
from rss_reader.src.rss_class import RssReader


class TestRssReader(unittest.TestCase):
    def setUp(self) -> None:
        print(f'Starting test {self._testMethodName}...')

    def tearDown(self) -> None:
        print(f'Ending test {self._testMethodName}...')

    def test_check_limit(self):
        """
        Checking the correctness of the method check_limit
        """
        rss = RssReader("http://rss.garant.ru/categories/news/", 1, False, False)
        self.assertEqual(RssReader.check_limit(rss), 1)

    def test_d(self):
        rss_dict = {'feed': 'FeedName',
                    'entries': [{'title': 'Title1',
                                 'date': 'Sun, 18 Sep 2022 17:09:00 +0300',
                                 'link': 'http://www.test.test',
                                 'summary': 'Summery1',
                                 'links': [{'index': 1,
                                            'href': 'http://www.test.test1',
                                            'type': 'text/html'},
                                           {'index': 2,
                                            'href': 'http://www.test.test1/460h4460.jpg', 'type': 'image/jpeg'}
                                           ]}
                                ]
                    }
        self.assertEqual(RssReader.print_rss(rss_dict), "1")


if __name__ == '__main__':
    unittest.main()
