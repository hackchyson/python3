# coding=utf8
"""
@project: python3
@file: uniquewords2
@author: mike
@time: 2021/1/22
 
@function:
"""
import sys
import string
import collections

words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + '\'"'
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                words[word] += 1  # change part

for word in words:
    print('"{}" occurs {} times'.format(word, words[word]))


