# coding=utf8
"""
@project: python3
@file: get_int
@author: mike
@time: 2021/1/15
 
@function:
"""


def get_int(msg):
    while True:
        try:
            i = int(input(msg))
            return i
        except ValueError as err:
            print(err)


if __name__ == '__main__':
    age = get_int('enter your age: ')
