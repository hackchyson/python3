# coding=utf8
"""
@project: python3
@file: shallow_copy
@author: mike
@time: 2021/1/29
 
@function:
"""
x = [53, 68, ['A', 'B', 'C']]
y = x[:]
print('{:.^50}'.format('print(x,y)'))
print(x, y, sep='\n')

y[1] = 40
x[2][0] = 'Q'
print('{:.^50}'.format('print(x,y)'))
print(x, y, sep='\n')

"""
....................print(x,y)....................
[53, 68, ['A', 'B', 'C']]
[53, 68, ['A', 'B', 'C']]
....................print(x,y)....................
[53, 68, ['Q', 'B', 'C']]
[53, 40, ['Q', 'B', 'C']]
"""

import copy

x = [53, 68, ['A', 'B', 'C']]
y = copy.deepcopy(x)
y[1] = 40
x[2][0] = 'Q'
print('{:.^50}'.format('print(x,y)'))
print(x, y, sep='\n')
"""
....................print(x,y)....................
[53, 68, ['Q', 'B', 'C']]
[53, 40, ['A', 'B', 'C']]
"""
