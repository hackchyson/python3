# coding=utf8
"""
@project: python3
@file: exception
@author: mike
@time: 2021/2/2
 
@function:
"""


def lst_find(lst, target):
    try:
        index = lst.index(target)
    except ValueError:
        index = -1
    return index
