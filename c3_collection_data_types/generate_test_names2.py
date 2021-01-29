# coding=utf8
"""
@project: python3
@file: generate_test_names2
@author: mike
@time: 2021/1/29
 
@function:
"""
import random


def get_forenames_and_surnames():
    forenames = []
    surnames = []
    for names, filename in ((forenames, 'data/forenames.txt'),
                            (surnames, 'data/surnames.txt')):
        for name in open(filename):
            names.append(name.rstrip())

    return forenames, surnames


forenames, surnames = get_forenames_and_surnames()
fh = open('test-names2.txt', 'w')

limit = 100
years = list(range(1970, 2013)) * 3
for year, forename, surname in zip(random.sample(years, limit),
                                   random.sample(forenames, limit),
                                   random.sample(surnames, limit)
                                   ):
    name = '{} {}'.format(forename, surname)
    fh.write('{:.<25}.{}\n'.format(name, year))
