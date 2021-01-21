# coding=utf8
"""
@project: python3
@file: unpacking
@author: mike
@time: 2021/1/20
 
@function:
"""
a = list(range(10))
first, *last = a
print(first, last)

first, *middle, last = a
print(first, middle, last)

*first, last = a
print(first, last)


