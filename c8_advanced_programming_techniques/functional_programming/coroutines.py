# If we want to perform a set of independent operations on some data, the
# conventional approach is to apply each operation in turn. The disadvantage of
# this is that if one of the operations is slow, the program as a whole must wait
# for the operation to complete before going on to the next one. A solution to this
# is to use coroutines.
import re
import functools
import sys

URL_RE = re.compile(r'''href=(?P<quote>['"])(?P<url>[^\1]+?)(?P=quote)''', re.IGNORECASE)
flags = re.MULTILINE | re.IGNORECASE | re.DOTALL
H1_RE = re.compile(r'<h1>(?P<h1>.+?)</h1>', flags)
H2_RE = re.compile(r'<h2>(?P<h2>.+?)</h2>', flags)


# There is one tiny problem with the (undecorated) matcher—when it is first
# created it should commence execution so that it advances to the yield ready to
# receive its first text. We could do this by calling the built-in next() function on
# each coroutine we create before sending it any data. But for convenience we
# have created the @coroutine decorator to do this for us.
def coroutine(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator

    return wrapper


@coroutine  # good decorator
def regex_matcher(receiver, regex):
    while True:
        text = (yield)  # suspends execution waiting for the yield expression
        for match in regex.finditer(text):
            receiver.send(match)


@coroutine
def reporter():
    ignore = frozenset({'style.css', 'index.html'})
    while True:
        match = (yield)
        if match is not None:
            groups = match.groupdict()
            if 'url' in groups and groups['url'] not in ignore:
                print('    URL:', groups['url'])
            elif 'h1' in groups:
                print('    H1:', groups['h1'])
            elif 'h2' in groups:
                print('    H2:', groups['h2'])


if __name__ == '__main__':

    receiver = reporter()
    matchers = (regex_matcher(receiver, URL_RE),
                regex_matcher(receiver, H1_RE),
                regex_matcher(receiver, H2_RE))

    try:
        for file in sys.argv[1:]:
            print(file)
            html = open(file, encoding='utf8').read()
            for matcher in matchers:
                matcher.send(html)
    finally:
        for matcher in matchers:
            matcher.close()
        receiver.close()
