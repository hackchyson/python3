# coding=utf8
"""
@project: python3
@file: binary_search
@author: mike
@time: 2021/1/21
 
@function:
"""
import bisect


def binary_search_bisect(lst, val):
    i = bisect.bisect(lst, val)
    try:
        if lst[i - 1] == val:
            return i - 1
    except IndexError:
        pass


def binary_search_bisect_left(lst, val):
    i = bisect.bisect_left(lst, val)
    try:
        if lst[i + 1] == val:
            return i
    except IndexError:
        pass


x = [0, 0, 1, 1, 2, 2]
x = [-1, 0, 0, 1, 2, 3, 4]
print(x)
for i in x:
    index = binary_search_bisect(x, i)
    print(index)
    index = binary_search_bisect_left(x, i)
    print(index)

print(binary_search_bisect(x, -5))
print(binary_search_bisect(x, 10))
