import logging
import argparse
import functools
import sys
import os
from fpdf import FPDF

from reader.rss_exeptions import RssReaderException, RssReaderHtmlException, RssReaderPdfException, RssReaderCacheException

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

__JSON_FILE__ = "data/news.json"


def parse_argument():
    """
    Parse and analyze command line arguments
    :return: command line arguments
    """
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument("--date",
                        help="News published date from cashes if this parameter provided",
                        type=int)

    nargs_source_value = "?" if ("--date" in sys.argv) else 1

    parser.add_argument("source",
                        help="RSS URL",
                        type=str,
                        nargs=nargs_source_value)

    parser.add_argument("--version",
                        action="version",
                        version="Version 1.4",
                        help="Print version info")

    parser.add_argument("--json",
                        help="Print result as JSON in stdout",
                        action="store_true")

    parser.add_argument("--verbose",
                        help="Outputs verbose status messages",
                        action="store_true")

    parser.add_argument("--limit",
                        help="Limit news topics if this parameter provided",
                        type=int)

    parser.add_argument("--to-html",
                        help="Pass to output html file",
                        type=str)

    parser.add_argument("--to-pdf",
                        help="Pass to output pdf file",
                        type=str)

    return parser.parse_args()


def get_logger(verbose: bool = True) -> logging.Logger:
    """
    Create a logger with stdout logging or in a file and returns Logger object
    :param verbose: if true then stdout logging
    :return: Logger instance
    """
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

    handler = logging.FileHandler("logfile.log")
    if verbose:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("The rss-reading starts working")

    return logger


def exceptions_suppressing_decorator(func):
    """
    This is a decorator that suppresses errors if they occur during the method
    :param func: specific method
    :return: wrapper
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except RssReaderException as exc:
            print("Please, check the entered parameters and start over. \n"
                  "The following exception was suppressed: " + exc.__str__())
            return None
        except RssReaderCacheException as exc:
            print("Please, check the file existence and start over. \n"
                  "The following exception was suppressed: " + exc.__str__())
            return None
        except RssReaderHtmlException as exc:
            print("Please, check the entered path to html and start over. \n"
                  "The following exception was suppressed: " + exc.__str__())
            return None
        except RssReaderPdfException as exc:
            print("Please, check the entered path to pdf and start over. \n"
                  "The following exception was suppressed: " + exc.__str__())
            return None
    return wrapper


def log_decorator(_func=None):
    """
    It is a log decorator for outputting to the log information about begin and end of the method,
    as well as the incoming parameters and the returned result.
    :param _func: specific method
    :return: log_decorator_wrapper
    """
    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(self, *args, **kwargs):
            logger_obj = self.logger_obj
            args_passed_in_function = [repr(a) for a in args]
            kwargs_passed_in_function = [f"{k}={v!r}" for k, v in kwargs.items()]
            formatted_arguments = ", ".join(args_passed_in_function + kwargs_passed_in_function)
            logger_obj.info(f"Begin function {func.__name__}() - Arguments: {str(formatted_arguments).encode('cp850', errors='replace')}")
            try:
                result = func(self, *args, **kwargs)
                logger_obj.info(f"End function {func.__name__}() - Returned: {str(result).encode('cp850', errors='replace')!r}")
                return result
            except Exception as exc:
                logger_obj.error(f"Exception: {exc.__str__()}")
                print("Something went wrong...")
                raise RssReaderException(exc.__str__())

        return log_decorator_wrapper

    if _func is None:
        return log_decorator_info
    else:
        return log_decorator_info(_func)


@exceptions_suppressing_decorator
def pass_to_html(html_path, rss_json):
    """
    Convert rss-news to html file
    :param html_path: path to html file
    :param rss_json: data with rss news in json format
    """
    try:
        with open(html_path, "w", encoding="utf-8") as outfile:
            html_template = """<html>
          <head>
          <title>RSS-reader</title>
          <meta charset="utf-8">
          </head>
          <body>
          """

            for entry in rss_json['entries']:
                keys_entry = entry.keys()
                html_template += f"<h1>{entry['feed']}</h1>"
                html_template += f"<h2>{entry['title']}</h2>"
                html_template += f"<p>{entry['date']}</p>"
                for link in entry['links']:
                    if link['type'] == 'image/jpeg':
                        html_template += f"<img src='{link['href']}'/>"

                if "summary" in keys_entry:
                    html_template += f"<p>{entry['summary']}</p>"
                html_template += f"<a href='{entry['link']}'>More details ...</a>"

            html_template += """
          </body>
          </html>
          """
            outfile.write(html_template)
    except Exception as exc:
        print(f"\nError: Unable to write html-file.")
        raise RssReaderHtmlException(exc.__str__())


@exceptions_suppressing_decorator
def pass_to_pdf(pdf_path, rss_json):
    """
    Convert rss-news to pdf file
    :param pdf_path: path to html file
    :param rss_json: data with rss news in json format
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', fname='data/DejaVuSerif-Bold.ttf')
        pdf.set_font('DejaVu', size=14)

        for entry in rss_json['entries']:
            keys_entry = entry.keys()
            pdf.write(txt=f"\n\nFeed: {entry['feed']}")
            pdf.write(txt=f"\n\nTitle: {entry['title']}")
            pdf.write(txt=f"\n\nDate: {entry['date']}")
            if "summary" in keys_entry:
                pdf.write(txt=f"\n\nSummary: {entry['summary']}")
            pdf.write(txt=f"\n\n")
            pdf.cell(txt="See more details ...", border=1, align="C", link=f"{entry['link']}")
            pdf.write(txt=f"\n\n\n--------------------------")
        pdf.output(pdf_path)
    except Exception as exc:
        print(f"\nError: Unable to write pdf-file.")
        raise RssReaderPdfException(exc.__str__())

