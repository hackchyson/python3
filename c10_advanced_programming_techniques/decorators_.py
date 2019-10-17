import logging
import functools
import tempfile
import os


def positive_result(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper


def positive_result_v2(function):
    @functools.wraps(function)
    # simplify
    # wrapper.__name__ = function.__name__
    # wrapper.__doc__ = function.__doc__

    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    return wrapper


@positive_result_v2
def discriminate(a, b, c):
    return (b ** 2) - (4 * a * c)


# In some cases it would be useful to be able to parameterize a decorator, but at
# first sight this does not seem possible since a decorator takes just one argument,
# a function or method. But there is a neat solution to this. We can call a
# function with the parameters we want and that returns a decorator which can
# then decorate the function that follows it.
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
    return (amount / total) * 100


if __debug__:
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(tempfile.gettempdir(), 'logged.log'))

    logger.addHandler(handler)


    def logged(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            log = 'called: ' + function.__name__ + '('
            log += ', '.join(
                ['{0!r}'.format(a) for a in args] + ['{0!s}={1!r}'.format(k, v) for k, v in kwargs.items()])
            result = exception = None
            try:
                result = function(*args, *kwargs)
                return result
            except Exception as err:
                exception = err
            finally:
                log += (
                    (') -> ' + str(result)) if exception is None else ') {0}: {1}'.format(type(exception), exception))
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
@positive_result_v2
def helloworld(x):
    return x


if __name__ == '__main__':
    root = discriminate(1, 4, 3)
    print(root)  # 4
    # root = discriminate(1, 2, 3)  # AssertionError: discriminate() result isn't >=0

    p = percent(-1, 100)
    print(p)  # 0
    p = percent(101, 100)
    print(p)  # 100
    p = percent(50, 100)
    print(p)

    # logging.basicConfig(level=logging.DEBUG)
    discounted_price(100, 30)

    # helloworld(-1)  # AssertionError: helloworld() result isn't >=0
    helloworld(50)
    helloworld(101)
    print(__debug__)  # python -O
