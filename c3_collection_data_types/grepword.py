# coding=utf8
"""
@project: python3
@file: grepword
@author: mike
@time: 2021/1/29
 
@function:
"""
import sys

if len(sys.argv) < 3:
    print('usage: {} word infile1 [infile2 [... infileN]]')
    sys.exit()
print(sys.argv)
word = sys.argv[1]
for filename in sys.argv[2:]:
    for lino, line in enumerate(open(filename), start=1):
        if word in line:
            print('{}:{}:{:.40}'.format(filename, lino, line.rstrip()))
