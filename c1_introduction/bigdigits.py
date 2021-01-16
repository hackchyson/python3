# coding=utf8
"""
@project: python3
@file: bigdigits
@author: mike
@time: 2021/1/15
 
@function:
"""
# for commandline arguments
import sys

Zero = [
    '  ***  ',
    ' *   * ',
    '*     *',
    '*     *',
    '*     *',
    ' *   * ',
    '  ***  '
]
'''
One detail to note is that the Zero list of strings is spread over multiple lines. 
Python statements normally occupy a single line, but they can span multiple lines 
if they are a parenthesized expression, a list, set, or dictionary literal, a 
function call argument list, or a multiline statement where every end-of-line 
character except the last is escaped by preceding it with a backslash (\). 
In all these cases any number of lines can be spanned and indentation does not 
matter for the second and subsequent lines.
'''

One = [" * ", "** ", " * ", " * ", " * ", " * ", "***"]
Two = [" *** ", "*   *", "*  * ", "  *  ", " *   ", "*    ", "*****"]
Three = [" *** ", "*   *", "    *", "  ** ", "    *", "*   *", " *** "]
Four = ["   *  ", "  **  ", " * *  ", "*  *  ", "******", "   *  ", "   *  "]
Five = ["*****", "*    ", "*    ", " *** ", "    *", "*   *", " *** "]
Six = [" *** ", "*    ", "*    ", "**** ", "*   *", "*   *", " *** "]
Seven = ["*****", "    *", "   * ", "  *  ", " *   ", "*    ", "*    "]
Eight = [" *** ", "*   *", "*   *", " *** ", "*   *", "*   *", " *** "]
Nine = [" ****", "*   *", "*   *", " ****", "    *", "    *", "    *"]

Digits = [Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]

try:
    digits = sys.argv[1]
    row = 0
    while row < 7:  # each number has 7 elements
        line = ''
        column = 0
        while column < len(digits):  # iterate all number in commandline argument
            number = int(digits[column])
            digit = Digits[number]
            line += digit[row] + '  '
            column += 1
        print(line)
        row += 1
except IndexError:  # if there is no commandline argument
    print('usage: bigdigits.py <number>')
except ValueError as err: # if the argument is not a number
    print(err, 'in', digits)
