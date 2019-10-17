import builtins
import collections


class Point:
    # When a class is created without the use of __slots__ , behind the scenes Python
    # creates a private dictionary called __dict__ for each instance, and this dictionary
    # holds the instance’s data attributes. This is why we can add or remove attributes from objects.

    # If we only need objects where we access the original attributes and don’t need
    # to add or remove attributes, we can create classes that don’t have a __dict__ .
    # This is achieved simply by defining a class attribute called __slots__ whose
    # value is a tuple of attribute names. These objects consume less memory and are faster
    # than conventional objects.

    # If we inherit from a class that uses __slots__ we must declare
    # slots in our subclass, even if empty, such as __slots__
    # = () ; or the memory and speed savings will be lost.
    __slots__ = ('x', 'y')

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Ord:
    def __getattr__(self, item):
        # builtin.ord() works for any characters
        # class Ord work for characters that is a valid identifier
        return builtins.ord(item)


class Const:
    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise ValueError('cannot change a const attribute')
        self.__dict__[key] = value

    def __delattr__(self, item):
        if item in self.__dict__:
            raise ValueError('cannot delete a const attribute')
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))


if __name__ == '__main__':
    ord = Ord()
    print(ord.a)
    print(ord.Z)

    const = Const()
    const.limit = 591
    print(const.limit)
    # const.limit = 1
    # del const.limit

    Const = collections.namedtuple('_', 'min max')(191, 591)  # throwaway name for the named tuple
    print(Const.min, Const.max)
    Offset = collections.namedtuple('_', 'id name description')(*range(3))
    print(Offset.id, Offset.name, Offset.description)
