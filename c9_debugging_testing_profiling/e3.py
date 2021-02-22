#!/usr/bin/env python3
"""
@project: python3
@file: e3
@author: mike
@time: 2021/2/20
 
@function:
"""


def div():
    1 / 0


if __name__ == '__main__':
    div()

# Traceback (most recent call last):
#   File "/Users/mike/PycharmProjects/python3/c9_debugging_testing_profiling/e3.py", line 17, in <module>
#     div()
#   File "/Users/mike/PycharmProjects/python3/c9_debugging_testing_profiling/e3.py", line 13, in div
#     1 / 0
# ZeroDivisionError: division by zero
