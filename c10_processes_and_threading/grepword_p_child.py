#!/usr/bin/env python3
"""
@project: python3
@file: grepword_p_child
@author: mike
@time: 2021/2/22
 
@function:
"""
import sys

coding = 'utf8'
BLOCK_SIZE = 8000
number = f'{sys.argv[1]}' if len(sys.argv) == 2 else ''
stdin = sys.stdin.buffer.read()
lines = stdin.decode(coding, 'ignore').splitlines()
word = lines[0].rstrip()

for filename in lines[1:]:
    filename = filename.rstrip()
    previous = ''
    try:
        with open(filename, 'rb') as fh:
            while True:
                current = fh.read(BLOCK_SIZE)
                if not current:
                    break
                current = current.decode(coding, 'ignore')
                if word in current or word in previous[-len(word):] + current[:len(word)]:
                    print(f'{number}{filename}')
                    break
                if len(current) != BLOCK_SIZE:
                    break
                previous = current
    except EnvironmentError as err:
        print(f'{number}{err}')
