#!/usr/bin/env python3
"""
@project: python3
@file: Point
@author: mike
@time: 2021/2/8
 
@function:
"""


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def just(self):
        return True


class PointFixedAttribute:
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def just(self):
        return True


class SubP(PointFixedAttribute):

    def __init__(self, z):
        super().__init__()
        self.z = z


def just():
    just.cache = []
    # just.cache.append('hello')
    # just.cache.append('world')
    return just.cache


if __name__ == '__main__':
    pfa = PointFixedAttribute()
    p = Point()

    # print(pfa.__dict__)  # AttributeError: 'PointFixedAttribute' object has no attribute '__dict__'
    print(pfa.__slots__)  # ('x', 'y')
    print(p.__dict__)  # {'x': 0, 'y': 0}

    # pfa.z = 1  # AttributeError: 'PointFixedAttribute' object has no attribute 'z'
    p.z = 1
    print(p.z)  # 1
    print(p.__dict__)  # {'x': 0, 'y': 0, 'z': 1}

    print(Point.__dict__)

    print(just)
    print(just.__dict__)
    print(just())
    # print(just())

    print(pfa.just())

    subp = SubP(10)
    print(subp.x)
    print(subp.z)
