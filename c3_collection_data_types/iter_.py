# coding=utf8
"""
@project: python3
@file: iter_
@author: mike
@time: 2021/1/29
 
@function:
"""
n = 0


def print_num(n=0):
    print(n)
    n += 1


i = iter(print_num, 10)
next(i)
next(i)

product = 1
for i in [1, 2, 4, 8]:
    product *= i
print(product)

product = 1
i = iter([1, 2, 4, 8])
while True:
    try:
        product *= i
    except StopIteration:
        break
print(product)
