# Partial function application is the creation of a function from an existing
# function and some arguments to produce a new function that does what the
# original function did, but with some arguments fixed so that callers don’t have
# to pass them.
import functools

lines = list('abcdefg')
import tkinter


def process_line(i, line):
    print(i, line)


# useful
enumerate1 = functools.partial(enumerate, start=1)
for lino, line in enumerate1(lines):
    process_line(lino, line)

reader = functools.partial(open, mode='rt', encoding='utf8')
writer = functools.partial(open, mode='wt', encoding='utf8')
