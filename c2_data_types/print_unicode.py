# coding=utf8
"""
@project: python3
@file: print_unicode
@author: mike
@time: 2021/1/20
 
@function:
"""
import sys
import unicodedata

"""
@project: python3
@file: print_unicode
@author: mike
@time: 2021/1/20

@function:
"""


def print_unicode_table(word):
    print('decimal    hex   chr  {:^40}'.format('name'))
    print('-------   -----  ---  {:-<40}'.format(''))

    code = ord(' ')  # start
    end = 55295
    print(end)

    while code <= end:
        c = chr(code)
        name = unicodedata.name(c, '*** unknown ***')
        if word is None or word in name.lower():
            print('{0:7}  {0:5X}  {0:^3c}  {1}'.format(code, name.title()))
        code += 1


word = None
if len(sys.argv) > 1:  # there are commandline arguments
    if sys.argv[1] in ('-h', '--help'):
        print('usage: {0[0]} [string]'.format(sys.argv))
        word = 0  # flag the end of the program
    else:
        word = sys.argv[1].lower()
if word != 0:
    print_unicode_table(word)
