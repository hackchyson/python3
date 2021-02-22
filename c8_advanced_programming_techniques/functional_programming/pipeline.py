import os
import sys
import functools


def coroutine(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator

    return wrapper


@coroutine
def reporter():
    while True:
        filename = (yield)
        print(filename)


@coroutine
def get_files(receiver):
    """
    A wrapper of os.walk()
    :param receiver:
    :return:
    """
    while True:
        path = (yield)
        if os.path.isfile(path):
            receiver.send(os.path.abspath(path))
        else:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    receiver.send(os.path.abspath(os.path.join(root, filename)))


@coroutine
def suffix_matcher(receiver, suffixes):
    while True:
        filename = (yield)
        if filename.endswith(suffixes):
            receiver.send(filename)


@coroutine
def size_matcher(receiver, minimum=None, maximum=None):
    while True:
        filename = (yield)
        size = os.path.getsize(filename)
        if ((minimum is None or size >= minimum) and
                (maximum is None or size <= maximum)):
            receiver.send(filename)


if __name__ == '__main__':
    # notice the order in coroutine
    pipes = []
    pipes.append(reporter)
    pipes.append(size_matcher(pipes[-1], minimum=1024))
    pipes.append(suffix_matcher(pipes[-1], (".png", ".jpg", ".jpeg", ".py")))
    pipes.append(get_files(pipes[-1]))
    pipeline = pipes[-1]
    # Equal to
    # pipeline = get_files(suffix_matcher(size_matcher(reporter(), minimum=1024), (".png", ".jpg", ".jpeg", ".py")))

    try:
        for file in sys.argv[1:]:
            print(file)
            pipeline.send(file)
            # pipeline.py
            # /Users/mike/PycharmProjects/python3/c8_advanced_programming_techniques/functional_programming/pipeline.py
            # partial.py
            # /Users/mike/PycharmProjects/python3/c8_advanced_programming_techniques/functional_programming/partial.py
            # __init__.py
    finally:
        for pipe in pipes:
            pipe.close()
