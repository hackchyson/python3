# coding=utf8
"""
@project: python3
@file: generate_test_names1
@author: mike
@time: 2021/1/29
 
@function:
"""
import random


def get_forenames_and_surnames():
    forenames = []
    surnames = []
    # this manner, clear
    # Inside Python programs it is convenient to always use Unix-style paths,
    # since they can be typed without the need for escaping, and they work on all platforms (including Windows).
    # If we have a path we want to present to the user in, say, variable path,
    # we can always import the os module and call path.replace("/", os.sep) to replace forward slashes
    # with the platform-specific book_dir separator.
    for names, filename in ((forenames, 'data/forenames.txt'),
                            (surnames, 'data/surnames.txt')):
        for name in open(filename):
            names.append(name.rstrip())

    return forenames, surnames


forenames, surnames = get_forenames_and_surnames()
fh = open('test-names1.txt', 'w')
for i in range(100):
    line = '{} {}\n'.format(random.choice(forenames), random.choice(surnames))
    fh.write(line)
