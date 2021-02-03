# coding=utf8
"""
@project: python3
@file: scope
@author: mike
@time: 2021/2/3
 
@function:
"""

AUTHOR = 'Mike'  # global


def say_hello():  # global
    global language  # global
    language = 'fr'
    text = 'hello'  # local
    print(text)


class MyException(Exception):  # global
    pass


say_hello()
print(language)
