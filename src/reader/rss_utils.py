import logging
import argparse
import functools
from reader.rss_exeptions import RssReaderException


def parse_argument():
    """
    Parse and analyze command line arguments
    :return: command line arguments
    """
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument("source",
                        help="RSS URL",
                        type=str)

    parser.add_argument("--version",
                        action="version",
                        version="Version 1.1",
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
            logger_obj.info(f"Begin function {func.__name__}() - Arguments: {formatted_arguments}")
            try:
                result = func(self, *args, **kwargs)
                logger_obj.info(f"End function {func.__name__}() - Returned: {result!r}")
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
            print("Please, check the rss link and start over. \n"
                  "The following exception was suppressed: " + exc.__str__())
            return None

    return wrapper
