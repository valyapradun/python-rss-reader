import unittest
import sys
from os import path
from datetime import date
from unittest.mock import patch, call

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

from reader.rss_entities import RssReader
from reader.rss_utils import pass_to_html, pass_to_pdf

rss_json = {"entries": [{"rss_source": "http://test_news/",
                         "feed": "Test Feed",
                         "title": "Test Title",
                         "date": "2022-09-27 00:40:19+00:00",
                         "link": "https://test_news/1.html",
                         "links": [
                             {"index": 1,
                              "href": "https://test_news/1.html",
                              "type": "text/html"}]}]}


class TestRssReader(unittest.TestCase):
    def setUp(self) -> None:
        print(f'Starting test {self._testMethodName}...')

    def tearDown(self) -> None:
        print(f'Ending test {self._testMethodName}...')

    def test_check_limit_correct_value(self):
        """
        Checking the correctness of the method check_limit with correct value
        """
        rss = RssReader("http://rss.garant.ru/categories/news/", 1, False, False)
        self.assertEqual(RssReader.check_limit(rss), 1)

    def test_check_limit_incorrect_value(self):
        """
        Checking the correctness of the method check_limit with incorrect value
        """
        rss = RssReader("http://rss.garant.ru/categories/news/", 2, False, False)
        self.assertNotEqual(RssReader.check_limit(rss), 3)

    def test_read_cashed_news(self):
        """
        Checking the correctness of the method read_cashed_news
        """
        rss = RssReader(None, 2, False, False, 20220927)
        rss.cache_path = "data/test_cache.json"
        self.assertEqual(RssReader.read_cashed_news(rss), [])

    def test_check_date_incorrect_value(self):
        """
        Checking the correctness of the method check_date with incorrect value
        """
        rss = RssReader("http://rss.garant.ru/categories/news/", 2, False, False, 30000000)
        today = int(str(date.today()).replace('-', ''))
        self.assertEqual(RssReader.check_date(rss), today)

    def test_check_date_correct_value(self):
        """
        Checking the correctness of the method check_date with correct value
        """
        rss = RssReader("http://rss.garant.ru/categories/news/", 2, False, False, 20220926)
        self.assertEqual(RssReader.check_date(rss), 20220926)

    def test_pass_to_html(self):
        """
        Checking existing html file after running pass_to_html method
        """
        html_path = 'data/test.html'
        pass_to_html(html_path, rss_json)
        self.assertEqual(path.isfile(html_path), True)

    def test_pass_to_pdf(self):
        """
        Checking existing pdf file after running pass_to_pdf method
        """
        pdf_path = 'data/test.pdf'
        pass_to_pdf(pdf_path, rss_json)
        self.assertEqual(path.isfile(pdf_path), True)


@patch('builtins.print')
class TestMock(unittest.TestCase):
    def test_print_rss_json(self, print_mock):
        """
        Checking the correctness of print rss in json format
        """
        """Checking the correctness input ('8')"""
        rss = RssReader("http://test_news/", 1, True, False, 20220926)
        rss.print_rss(rss_json)
        print_mock.assert_called_once_with(rss_json)

    def test_print_rss_not_json(self, print_mock):
        """
        Checking the correctness of print rss in not json format
        """
        """Checking the correctness input ('8')"""
        rss = RssReader("http://test_news/", 1, False, False, 20220926)
        rss.print_rss(rss_json)
        print_mock.assert_called_with('[1]: https://test_news/1.html (text/html)')


if __name__ == '__main__':
    unittest.main()
