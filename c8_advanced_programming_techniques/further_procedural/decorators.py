#!/usr/bin/env python3
"""
@project: python3
@file: decorators
@author: mike
@time: 2021/2/7
 
@function:
"""
import functools
import logging
import os
import tempfile


# def positive_result(function):
#     def wrapper(*args, **kwargs):
#         result = function(*args, **kwargs)
#         assert result >= 0, function.__name__ + "() result isn't >= 0"
#         return result
#
#     wrapper.__name__ = function.__name__
#     wrapper.__doc__ = function.__doc__
#     return wrapper

def positive_result(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    return wrapper


@positive_result
def discriminant(a, b, c):
    return b ** 2 - 4 * a * c


def bounded(minimum, maximum):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result < minimum:
                return minimum
            elif result > maximum:
                return maximum
            return result

        return wrapper

    return decorator


@bounded(0, 100)
def percent(amount, total):
    return amount / total * 100


if __debug__:
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(tempfile.gettempdir(), 'logged.log'))

    logger.addHandler(handler)


    def logged(function):
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
    def logged(function):
        return function


@logged
def discounted_price(price, percentage, make_integer=False):
    result = price * ((100 - percentage) / 100)
    if not (0 < result <= price):
        raise ValueError('invalid price')
    return result if not make_integer else int(round(result))


# the order matters
@logged
@bounded(0, 100)
def just_x(x):
    return x


if __name__ == '__main__':
    discounted_price(1000, 5)
    just_x(-10)
    just_x(110)
    just_x(50)
