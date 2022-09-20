# [python-rss-reader](https://github.com/valyapradun/python-rss-reader)

## Description
This is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable 
format.

## Usage
**python-rss-reader** has an easy-to-use user interface to get started. 

If the `--json` argument is used, the utility will convert the news to the [JSON](https://en.wikipedia.org/wiki/JSON) 
format in the following structure:
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

## Start and Installation

You can run rss_reader _both_ with and without installation of CLI utility, but no matter how you run it, 
you need to install the Python _feedparser_ module, which will be used to parse rss. 
To do this, please type in your terminal:
```
> pip install feedparser
```

After that, you can choose the run method yourself, meaning that this should work:

Way 1 (without installation of CLI utility):
```
> python src/rss_reader/rss_reader.py ...
```

as well as this: 

Way 2 (wit installation of CLI utility):
```
> rss_reader ...
```

To run using _Way 2_:

* step 1: you need to install _build_ using pip:
```
> pip install --upgrade build
```
* step 2: previous command will allow you to run the commands: 
```
> python -m build
```

```
> python -m pip install -e .
```
* step 3: previous command will allow you to run the commands: 


*>pip install --upgrade setuptools*



*>python src/rss_reader/rss_reader.py*

