# coding=utf8
"""
@project: python3
@file: assert_
@author: mike
@time: 2021/2/3
 
@function:
"""


def product(*args):  # pessimistic
    assert all(args), "0 argument"
    result = 1
    for arg in args:
        result *= arg
    return result


lst = list(range(10))
print(product(*lst))


def ha():
    """
    One line description.

    Detail description.

    >>> ha()
    'hello'
    >>> ha()
    'world'

    :return:
    """
    return 'hello'


print(ha())
