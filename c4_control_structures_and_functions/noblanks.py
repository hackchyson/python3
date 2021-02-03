# coding=utf8
"""
@project: python3
@file: noblanks
@author: mike
@time: 2021/2/2
 
@function:
"""


def read_data(filename):
    lines = []
    fh = None
    try:
        fh = open(filename)
        for line in fh:
            if line.strip():
                lines.append(line)
    except (IOError, OSError) as err:
        print(err)
        return []
    finally:
        if fh is not None:
            fh.close()
    return lines


def find_word(table, target):
    found = False
    for row, record in enumerate(table):
        for column, field in enumerate(record):
            for index, item in enumerate(field):
                if item == target:
                    found = True
                    break
            if found:
                break
        if found:
            break

    if found:
        print('found at ({}, {}, {})'.format(row, column, index))
    else:
        print('not found')


def find_word2(table, target):
    class FoundException(Exception):
        pass

    try:
        for row, record in enumerate(table):
            for column, field in enumerate(record):
                for index, item in enumerate(field):
                    if item == target:
                        raise FoundException
    except FoundException:
        print('found at ({}, {}, {})'.format(row, column, index))
    else:
        print('not found')
