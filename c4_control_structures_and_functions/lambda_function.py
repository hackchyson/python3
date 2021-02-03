# coding=utf8
"""
@project: python3
@file: lambda_function
@author: mike
@time: 2021/2/3
 
@function:
"""
lst = list(range(-3, 3))
print(lst)
print(sorted(lst, key=lambda x: x ** 2))
print(sorted(lst, key=lambda key=None: key ** 2))  # seldom used

# [-3, -2, -1, 0, 1, 2]
# [0, -1, 1, -2, 2, -3]
# [0, -1, 1, -2, 2, -3]


s = lambda x: '' if x == 1 else 's'  # use def instead
print(s(1))  #
print(s(2))  # s

p = lambda key='hello': print(key)  # use def instead
p('world')  # world
