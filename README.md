# [python-rss-reader](https://github.com/valyapradun/python-rss-reader)

## Description
This is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable 
format or in json format. Each time the rss is read, the data is cached into the file, so that later it is possible 
to read the data from the cache. It is also possible to pass data to hml or pdf files.

## Start and Deployment

You can run the application _both_ with and without installation of CLI utility, meaning that it will work:

_Way 1 (run python code directly):_
```
> python src/reader/rss_reader.py ...  
```

as well as this:  

_Way 2 (run using CLI utility):_
```
> rss_reader ...
```

To run the __python code directly__, you need to additionally install the following using pip:

```
> python -m pip install feedparser
> python -m pip install dateutils
> python -m pip install pandas
> python -m pip install fpdf2
```

In order to start using the __CLI utility__, you need to do the following steps to install it correctly. 
Go to the main directory of the rss-reader (_python-rss-reader_) and run the following using pip:
* step 1: you need to install _build_ using pip:
```
> pip install --upgrade build
```
* step 2: previous command will allow you to run the commands: 
```
> python -m build
```
* step 3: and finally install the utility package: 
```
> python -m pip install -e .
```

Thereafter you can run rss_reader and you can choose the run method yourself.


## Usage
**python-rss-reader** has an easy-to-use user interface to get started. As a result, the news is displayed 
in the following form on the screen:
```shell
$ python src/reader/rss_reader.py "http://rss.garant.ru/categories/news" --limit 1

----------------------

Rss_source: http://rss.garant.ru/categories/news
Feed: Новости
Title: "Санитарные" категории риска для роддомов и перинатальных центров изменить нельзя
Date: 2022-09-20 11:23:00+03:00
Link: http://www.garant.ru/news/1567169/
Summary: Такой ответ дал Роспотребнадзор в соответствующем письме.

Links:
[1]: http://www.garant.ru/news/1567169/ (text/html)
[2]: http://www.garant.ru/files/9/6/1567169/sanitarnie_kategorii_460.jpg (image/jpeg)

```

Utility provides the following interface:
```shell
$ python src/reader/rss_reader.py --help
usage: rss_reader.py [-h] [--date DATE] [--version] [--json] [--verbose] [--limit LIMIT] [--to-html TO_HTML] [--to-pdf TO_PDF] source

Pure Python command-line RSS reader.

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --date DATE        News published date from cashes if this parameter provided
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --to-html TO_HTML  Pass to output html file
  --to-pdf TO_PDF    Pass to output pdf file
```

* `source`: this is a required argument that contains the RSS URL in quotation marks, for example:
_"http://rss.garant.ru/categories/news/"_, _"https://timesofindia.indiatimes.com/rssfeedstopstories.cms"_,
_"https://news.yahoo.com/rss/"_, etc.  
```
> python src/reader/rss_reader.py "http://rss.garant.ru/categories/news"
...
```

* `-h, --help` option: if this option is specified, app shows a help message with usage information and exit

* `--version` option: if this option is specified, app _just prints its version_ and stop. You can use this option 
without specifying RSS URL. For example:
```
> rss_reader --version
Version 1.4
```
* `--json` option: if the `--json` argument is used, the utility will convert the news to the 
[JSON](https://en.wikipedia.org/wiki/JSON) format in the following structure:
```
{'entries': [
     {
       'rss_source': 'https://news.yahoo.com/rss/',
       'feed': 'Yahoo News - Latest News & Headlines',
       'title': 'Greece gets first 2 upgraded F-16s out of a total 83',
       'date': '2022-09-12 17:00:00+03:00',
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
* `--verbose` option: if this parameter is not defined, the log file can be found as _logfile.log_ in the root directory
 of the project. If this option is specified, program prints all logs in stdout _in the process_ of application running. 
 For instance:
```
> rss_reader "http://rss.garant.ru/categories/news" --limit 1 --json --verbose

2022-09-20 21:26:29,765 - INFO - get_logger - The rss-reading starts working
2022-09-20 21:26:29,765 - INFO - log_decorator_wrapper - Begin function check_limit() - Arguments:
2022-09-20 21:26:29,766 - INFO - log_decorator_wrapper - End function check_limit() - Returned: 1
2022-09-20 21:26:29,766 - INFO - log_decorator_wrapper - Begin function parse_rss() - Arguments:
2022-09-20 21:26:29,767 - INFO - log_decorator_wrapper - End function parse_rss() - Returned: {'entries': ...}
...
2022-09-20 21:26:29,768 - INFO - log_decorator_wrapper - Begin function write_json() - Arguments: {'entries': ... }
...
2022-09-20 21:26:29,770 - INFO - log_decorator_wrapper - End function write_json() - Returned: None
2022-09-20 21:26:29,772 - INFO - log_decorator_wrapper - Begin function print_rss() - Arguments: {'entries': ... }
...
2022-09-20 21:26:29,774 - INFO - log_decorator_wrapper - End function print_rss() - Returned: None
```
* `--limit` option: if this option is provided, app limits news topics. If it is not specified, then app prints _all_ 
available feed. If this parameter is larger than feed size then app prints _all_ available news.

* `--date` option: if this option is specified, the cached news can be read with it. The news from the specified day 
will be printed out. Here date means actual *publishing date* not the date when you fetched the news. 

It should take a date in `%Y%m%d` format. 

```
> python src/reader/rss_reader.py --date 20220925
```

If this argument is not provided, the utility works like in the previous iterations. 

`--date` **doesn't** require internet connection to fetch news from local cache. The local cache is a __news.json__ file 
that is created in the _data/_ directory in the project's root directory. The file structure is similar to the structure
 described above in the `--json` parameter.

You can use `--date` without specifying RSS source. If it's specified _together with RSS source_, then app gets news 
_for this date_ from local cache that _were fetched from specified source_. 

```
> python src/reader/rss_reader.py "http://rss.garant.ru/categories/news" --date 20220925 --limit 2
```
 
`--date` works correctly with both `--json`, `--limit`, `--verbose` and their different combinations. 

If the news are not found, an error will be returned..
```
Error: no news for specified source (_INPUT_SOURCE_) or date (_INPUT_DATE_).
```

* `--to-html` option: if this option is specified, the utility will convert the news to html file. The path to the file 
in quotation marks defines this option. 

Final html file contains such fields as: 
feed, title, date, summary, clickable link (section _More details ..._) and pictures if they exist in the original article. 
For instance,

```
<html>
    <head>
        <title>RSS-reader</title>
        <meta charset="utf-8">
    </head>
        <body>
          <h1>Yahoo News - Latest News & Headlines</h1>
		  <h2>Drone attack hits Ukraine; US vows 'consequences' over nukes</h2>
		  <p>2022-09-26 07:15:12+00:00</p>
		  <a href='https://news.yahoo.com/drone-attack-hits-ukraine-us-071512186.html'>More details ...</a>
        </body>
</html>
```

This conversion option works with all the arguments that were described above. 

For example, the next run will print in human-readable format 3 news from the local cache where the date is 20220926 
and the source is "https://news.yahoo.com/rss/" (if they exists), and this result will also be saved 
to a file "data/news.html"

```
> python src/reader/rss_reader.py "https://news.yahoo.com/rss/" --date 20220926 --to-html "data/news.html" --limit 3

```

* `--to-pdf` option: if this option is specified, the utility will convert the news to pdf file. The path to the file 
in quotation marks defines this option. 

Final pdf file contains such fields as: 
feed, title, date, summary, clickable link (section _See more details ..._) if they exist in the original article.

For instance,

```
Feed: Yahoo News - Latest News & Headlines
Title: Drone attack hits Ukraine; US vows 'consequences' over
nukes
Date: 2022-09-26 07:15:12+00:00
See more details ...
--------------------------
Feed: Yahoo News - Latest News & Headlines
Title: Meghan Did “Desperately Unhappy” Harry the “Greatest
Kindness” by Getting Him Out of Royal Life
Date: 2022-09-26 08:44:44+00:00
See more details ...
--------------------------
```

This conversion option works with all the arguments that were described above. 

For example, the next run will print in json format 2 news from the local cache where the date is 20220926 
and the source is "https://news.yahoo.com/rss/" (if they exists), and this result will also be saved to a file 
"data/news.pdf"

```
> python src/reader/rss_reader.py "https://news.yahoo.com/rss/" --date 20220926 --to-pdf "data/news.pdf" --limit 2 --json

```