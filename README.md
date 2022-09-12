# [python-rss-reader](https://github.com/valyapradun/python-rss-reader)

## Description
This is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable format.

## Usage
**python-rss-reader** has an easy-to-use user interface to get started. 

If the `--json` argument is used, the utility will convert the news to the [JSON](https://en.wikipedia.org/wiki/JSON) format in the following structure:
```
{
  'feed': 'Yahoo News - Latest News & Headlines',
  'entries': [
     {
       'title': 'Greece gets first 2 upgraded F-16s out of a total 83',
       'date': '2022-09-12T17:00:09Z',
       'link': 'https://news.yahoo.com/greece-gets-first-2-upgraded-170009306.html',
       'summary': 'Greece gets first 2 upgraded F-16s out of a total 83',
       'links': [
            {
               'index': 1,
               'href': 'https://news.yahoo.com/greece-gets-first-2-upgraded-170009306.html',
               'type': 'text/html'
            },
            {
               'index': 2,
               'href': 'http://news.yahoo.com/greece-gets-first-2-upgraded-170009306_460_460.jpg',
               'type': 'image/jpeg'
            }
        ]
      }
   ]
}
```

## Installation
You need to install the following before using:

*pip install feedparser*