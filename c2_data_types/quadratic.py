# coding=utf8
"""
@project: python3
@file: quadratic
@author: mike
@time: 2021/1/20
 
@function:
"""
import cmath
import math
import sys


def get_float(msg, allow_zero):
    x = None
    while x is None:
        try:
            x = float(input(msg))
            if not allow_zero and abs(x) < sys.float_info.epsilon:
                print('zero is not allowed')
                x = None
        except ValueError as err:
            print(err)
    return x


print('ax\N{superscript two} + bx + c = 0')
a = get_float('Enter a: ', False)
b = get_float('Endter b: ', True)
c = get_float('Enter c: ', True)

x1 = None
x2 = None
discriminant = (b ** 2) - (4 * a * c)
if discriminant == 0:
    x1 = -(b / (2 * a))
else:
    if discriminant > 0:
        root = math.sqrt(discriminant)
    else:
        root = cmath.sqrt(discriminant)
    x1 = (-b + root) / (2 * a)
    x2 = (-b - root) / (2 * a)

equation = ('{a}x\N{superscript two} {b:+}x {c:+} = 0'
            ' \N{rightwards arrow} x = {x1}').format(**locals())
if x2 is not None:
    equation += ' or x = {x2}'.format(**locals())
print(equation)
