# coding=utf8
"""
@project: python3
@file: uniquewords1
@author: mike
@time: 2021/1/21
 
@function:
"""
import sys
import string

words = {}
strip = string.whitespace + string.punctuation + string.digits + '\'"'
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                words[word] = words.get(word, 0) + 1

for word in words:
    print('"{}" occurs {} times'.format(word, words[word]))
