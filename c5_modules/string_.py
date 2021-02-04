# coding=utf8
"""
@project: python3
@file: string
@author: mike
@time: 2021/2/4
 
@function:
"""
import sys
import io

print('hello', file=sys.stdout)
print('hello', file=sys.stderr)
sys.stdout.write('world')

fh = open('text.txt', 'w')
print('hello world', file=fh)

string_io = io.StringIO()
sys.stdout = string_io

for i in range(100):
    print('hello' + i)

sys.stdout = sys.__stdout__  # recover the default sys.stdout
print(string_io.getvalue())  # get the value in string io
