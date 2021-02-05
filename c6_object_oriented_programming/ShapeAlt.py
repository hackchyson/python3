#!/usr/bin/env python3

import math


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def distance_from_origin(self):
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Point({self.x!r}, {self.y!r})'

    def __str__(self):
        return f'({self.x!r}, {self.y!r})'


class Circle(Point):
    def __init__(self, radius, x=0, y=0):
        super().__init__(x, y)
        self.radius = radius

    @property
    def edge_distance_from_origin(self):
        return abs(self.distance_from_origin - self.radius)

    @property
    def area(self):
        return math.pi * (self.radius ** 2)

    @property
    def circumference(self):
        return 2 * math.pi * self.radius

    @property
    def radius(self):
        return self.__radius

    @property.setter
    def radius(self, radius):
        assert radius > 0, 'radius must be nonzero and non-negative'
        self.__radius = radius

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius and super().__eq__(other)

    def __repr__(self):
        return f'Circle({self.radius!r}, {self.x!r}, {self.y!r})'

    def __str__(self):
        return repr(self)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
