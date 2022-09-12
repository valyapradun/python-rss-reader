import functools


def exceptions_suppressing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as exc:
            print('Please check if the link is correct and try again. \nThe following exception was suppressed: ' + exc.__str__())
            return None
    return wrapper
