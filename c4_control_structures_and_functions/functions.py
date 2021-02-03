# coding=utf8
"""
@project: python3
@file: functions
@author: mike
@time: 2021/2/3
 
@function:
"""

import math


def my_sum(a, b, c=1):
    return a + b + c


print(my_sum(1, 2, 3))
print(my_sum(1, 2))


def append_if_even(x, lst=[]):
    if x % 2 == 0:
        lst.append(x)
    return lst


def append_if_even2(x, lst=None):
    lst = [] if lst is None else lst
    if x % 2 == 0:
        lst.append(x)
    return lst


for i in range(3):
    result1 = append_if_even(i)
    result2 = append_if_even2(i)
    print(f'{result1=},{i=}')
    print(f'{result2=},{i=}')


def say_hello(text='hello'):
    """
    Print text.

    :param text: text should be printed
    :return: None
    """
    print(text)


def shorten(text, length=25, indicator="..."):
    """Returns text or a truncated copy with the indicator added

    text is any string; length is the maximum length of the returned
    string (including any indicator); indicator is the string added at
    the end to indicate that the text has been shortened

    >>> shorten("Second Variety")
    'Second Variety'
    >>> shorten("Voices from the Street", 17)
    'Voices from th...'
    >>> shorten("Radio Free Albemuth", 10, "*")
    'Radio Fre*'
    """
    if len(text) > length:
        text = text[:length - len(indicator)] + indicator
    return text


print(shorten("Voices from the Street", 17))

print(my_sum(*[1, 2, 3, 4][:3]))
print(my_sum(*[1, 2], **{'c': 3}))


def product(*args):
    result = 1
    for arg in args:
        result *= arg
    return result


print(product(*list(range(1, 10))))
print(math.factorial(9))


# We can have keyword arguments following positional arguments
def sum_of_powers(*args, power=1):
    result = 0
    for arg in args:
        result += arg ** power
    return result


# It is also possible to use * as a “parameter” in its own right.
# This is used to signify that there can be no positional arguments after the *.
def heron(a, b, c, *, units='square meters'):
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return f'{area} {units}'


print(heron(25, 24, 7))
print(heron(41, 9, 40, units="sq. inches"))


# print(heron(25, 24, 7, "sq. inches"))


def print_dict(**kwargs):
    for key in sorted(kwargs):
        print(f'{key:10} : {kwargs[key]}')


print_dict(**{str(i): f'{100 * i:3}%' for i in range(10)})


# 0          :   0%
# 1          : 100%
# 2          : 200%
# 3          : 300%
# 4          : 400%
# 5          : 500%
# 6          : 600%
# 7          : 700%
# 8          : 800%
# 9          : 900%

def print_args(*args, **kwargs):
    for i, arg in enumerate(args):
        print("positional argument {0} = {1}".format(i, arg))
    for key in kwargs:
        print("keyword argument {0} = {1}".format(key, kwargs[key]))


print_args(*list(range(10)), **locals())
