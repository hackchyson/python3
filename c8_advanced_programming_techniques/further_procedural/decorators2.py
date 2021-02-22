#!/usr/bin/env python3
"""
@project: python3
@file: decorators2
@author: mike
@time: 2021/2/8
 
@function:
"""
import logging
import functools
import os
import tempfile


def logged(file):
    """
    Log the output of the decorated function into a logged file.

    :param file: If file is None, use temple file, otherwise use the given file
    :return: decorated function
    """
    def decorator(function):
        if __debug__:
            logger = logging.getLogger('Logger')
            logger.setLevel(logging.DEBUG)
            if file is None:
                handler = logging.FileHandler(os.path.join(tempfile.gettempdir(), 'logged.log'))
            else:
                handler = logging.FileHandler(file)
            logger.addHandler(handler)

            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                # accumulate string
                log = 'called: ' + function.__name__ + '('
                log += ', '.join([f'{a!r}' for a in args] + [f'{k!s}={v!r}' for k, v in kwargs.items()])
                result = exception = None
                try:
                    result = function(*args, **kwargs)
                    return result
                except Exception as err:
                    exception = err
                finally:
                    log += (') -> ' + str(result)) if exception is None else f'{type(exception)}: {exception}'
                    logger.debug(log)
                    if exception is not None:
                        raise exception

            return wrapper
        else:
            return function

    return decorator


@logged(None)
def say_word(word='hello'):
    return word


if __name__ == '__main__':
    say_word('mike')
