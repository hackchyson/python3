import os
import sys

from chyson.decorators.coroutine import coroutine


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
    receiver = reporter()
    pipeline = size_matcher(receiver, minimum=1024)
    pipeline = suffix_matcher(pipeline, (".png", ".jpg", ".jpeg"))
    pipeline = get_files(pipeline)

    try:
        for file in sys.argv[1:]:
            print(file)
            pipeline.send(file)
    finally:
        pipeline.close()
        receiver.close()
