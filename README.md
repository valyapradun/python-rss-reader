# [python-rss-reader](https://github.com/valyapradun/python-rss-reader)

## Description
This is a command-line utility which receives [RSS](wikipedia.org/wiki/RSS) URL and prints results in human-readable 
format.

## Start and Deployment

In order to start using the utility, you need to do the following steps to install it correctly. 
Go to the main directory of the rss-reader (_python-rss-reader_) and run the following commands:
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

Thereafter you can run rss_reader and you can choose the run method yourself, meaning that this should work:

Way 1 (run python code):
```
> python src/rss_reader/rss_reader.py ...
```

as well as this: 

Way 2 (run using CLI utility):
```
> rss_reader ...
```

## Usage
**python-rss-reader** has an easy-to-use user interface to get started. As a result, the news is displayed 
in the following form on the screen:
```shell
$ python src/reader/rss_reader.py "http://rss.garant.ru/categories/news" --limit 1

Feed: Новости

----------------------

Title: "Санитарные" категории риска для роддомов и перинатальных центров изменить нельзя
Date: Tue, 20 Sep 2022 18:18:00 +0300
Link: http://www.garant.ru/news/1567169/
Summary: Такой ответ дал Роспотребнадзор в соответствующем письме.

Links:
[1]: http://www.garant.ru/news/1567169/ (text/html)
[2]: http://www.garant.ru/files/9/6/1567169/sanitarnie_kategorii_riska_dlya_roddomov_i_perinatalnih_tsentrov_izmenit_nelzya_460.jpg (image/jpeg)

```

Utility provides the following interface:
```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
```

* `-h, --help` option: if this option is specified, app shows a help message with usage information and exit

* `--version` option: if this option is specified, app _just prints its version_ and stop. You can use this option 
without specifying RSS URL. For example:
```
> rss_reader --version
Version 1.2
```
* `--json` option: if the `--json` argument is used, the utility will convert the news to the 
[JSON](https://en.wikipedia.org/wiki/JSON) format in the following structure:
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
* `--verbose` option: if this option is specified, program prints all logs in stdout _in the process_ 
of application running. For instance:
```
> rss_reader "http://rss.garant.ru/categories/news" --limit 1 --json --verbose

2022-09-20 21:26:29,765 - INFO - get_logger - The rss-reading starts working
2022-09-20 21:26:29,765 - INFO - log_decorator_wrapper - Begin function check_limit() - Arguments:
2022-09-20 21:26:29,766 - INFO - log_decorator_wrapper - End function check_limit() - Returned: 1
2022-09-20 21:26:29,766 - INFO - log_decorator_wrapper - Begin function parse_rss() - Arguments:
2022-09-20 21:26:29,766 - INFO - log_decorator_wrapper - End function parse_rss() - Returned: {'feed': 'Новости', 'entries': [{'title': '"Санитарные" категории риска для роддомов и перинатальных центров изменить нельзя', 'date': 'Tue,
20 Sep 2022 18:18:00 +0300', 'link': 'http://www.garant.ru/news/1567169/', 'summary': 'Такой ответ дал Роспотребнадзор в соответствующем письме.', 'links': [{'index': 1, 'href': 'http://www.garant.ru/news/1567169/', 'type': 'text/html'
}, {'index': 2, 'href': 'http://www.garant.ru/files/9/6/1567169/sanitarnie_kategorii_riska_dlya_roddomov_i_perinatalnih_tsentrov_izmenit_nelzya_460.jpg', 'type': 'image/jpeg'}]}]}
2022-09-20 21:26:29,767 - INFO - log_decorator_wrapper - Begin function print_rss() - Arguments: {'feed': 'Новости', 'entries': [{'title': '"Санитарные" категории риска для роддомов и перинатальных центров изменить нельзя', 'date': 'Tu
e, 20 Sep 2022 18:18:00 +0300', 'link': 'http://www.garant.ru/news/1567169/', 'summary': 'Такой ответ дал Роспотребнадзор в соответствующем письме.', 'links': [{'index': 1, 'href': 'http://www.garant.ru/news/1567169/', 'type': 'text/ht
ml'}, {'index': 2, 'href': 'http://www.garant.ru/files/9/6/1567169/sanitarnie_kategorii_riska_dlya_roddomov_i_perinatalnih_tsentrov_izmenit_nelzya_460.jpg', 'type': 'image/jpeg'}]}]}
{'feed': 'Новости', 'entries': [{'title': '"Санитарные" категории риска для роддомов и перинатальных центров изменить нельзя', 'date': 'Tue, 20 Sep 2022 18:18:00 +0300', 'link': 'http://www.garant.ru/news/1567169/', 'summary': 'Такой о
твет дал Роспотребнадзор в соответствующем письме.', 'links': [{'index': 1, 'href': 'http://www.garant.ru/news/1567169/', 'type': 'text/html'}, {'index': 2, 'href': 'http://www.garant.ru/files/9/6/1567169/sanitarnie_kategorii_riska_dly
a_roddomov_i_perinatalnih_tsentrov_izmenit_nelzya_460.jpg', 'type': 'image/jpeg'}]}]}
2022-09-20 21:26:29,770 - INFO - log_decorator_wrapper - End function print_rss() - Returned: None
```
* `--limit` option: if this option is provided, app limits news topics. If it is not specified, then app prints _all_ 
available feed. If this parameter is larger than feed size then app prints _all_ available news.



