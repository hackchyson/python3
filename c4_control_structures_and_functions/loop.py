# coding=utf8
"""
@project: python3
@file: loop
@author: mike
@time: 2021/2/2
 
@function:
"""

i = 0
while i < 100:
    i += 1
else:
    last = i
print(last)


def list_find(lst, target):
    """
    Find the first target's index or -1 if not find.

    :param lst:
    :param target:
    :return: index of the target if found or -1 if not found
    """
    index = 0
    while index < len(lst):
        if lst[index] == target:
            break
        index += 1
    else:
        index = -1
    return index


def list_find2(lst, target):
    for index, x in enumerate(lst):
        if x == target:
            break
    else:
        index = -1
    return index
