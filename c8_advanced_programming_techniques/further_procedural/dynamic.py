#!/usr/bin/env python3
"""
@project: python3
@file: dynamic
@author: mike
@time: 2021/2/7
 
@function:
"""
import math

# eval
x = eval('2 ** 10')
print(x)  # 1024

# exec
code = '''
def area_of_sphere(r):
    return 4 * math.pi * r ** 2
'''
# context = {}
# context['math'] = math
# exec(code, context)  # define the function area_of_sphere
context = globals().copy()
exec(code, context)

area_of_sphere = context['area_of_sphere']
sphere = area_of_sphere(5)
print(sphere)  # 314.1592653589793
