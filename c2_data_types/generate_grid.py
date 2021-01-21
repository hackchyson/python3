# coding=utf8
"""
@project: python3
@file: generate_grid
@author: mike
@time: 2021/1/16
 
@function:
"""
import random


def get_int(msg, minimum, default):
    while True:
        try:
            line = input(msg)
            # no input but there is a default
            if not line and default is not None:
                return default
            i = int(line)
            if i < minimum:
                print('must be >=', minimum)
            else:
                return i
        except ValueError as err:
            print(err)


rows = get_int('rows: ', 1, None)
columns = get_int('columns: ', 1, None)
minimum = get_int('minimum (or Enter for 0): ', -1000000, 0)

default = 1000
if default < minimum:
    default = 2 * minimum
maximum = get_int('maximum (or Enter for ' + str(default) + '): ', minimum, default)
num_len = len(str(maximum)) + 2

row = 0
while row < rows:
    line = ''
    column = 0
    while column < columns:
        i = random.randint(minimum, maximum)
        s = str(i)
        # for pretty printing
        while len(s) < num_len:
            s = ' ' + s
        line += s
        column += 1
    print(line)
    row += 1
