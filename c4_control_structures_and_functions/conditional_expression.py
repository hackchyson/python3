# coding=utf8
"""
@project: python3
@file: conditional_expression
@author: mike
@time: 2021/2/2
 
@function:
"""
for margin in range(3):
    width = 100 + (10 if margin else 0)
    print(width)

for count in range(5):
    print('{} file{}'.format(count if count != 0 else 'no', 's' if count != 1 else ''))
