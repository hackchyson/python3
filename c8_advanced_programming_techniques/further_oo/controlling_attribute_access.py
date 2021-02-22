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
        # builtin.ord() is used to avoid ord is used my the user
        # like ord = Ord()
        return builtins.ord(item)


class Const:
    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise ValueError('cannot change a const attribute')
        self.__dict__[key] = value

    def __delattr__(self, item):
        if item in self.__dict__:
            raise ValueError('cannot delete a const attribute')
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


USE_GETATTR = True


class Image:
    def __init__(self, width, height, filename="", background="#FFFFFF"):
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__width = width
        self.__height = height
        self.__colors = {self.__background}

    if USE_GETATTR:
        def __getattr__(self, name):
            if name == 'color':
                return set(self.__colors)
            classname = self.__class__.__name__
            if name in frozenset({'background', 'width', 'height'}):
                # image = Image(10, 10)
                # image.__dict__
                # {'filename': '',
                #  '_Image__background': '#FFFFFF',
                #  '_Image__data': {},
                #  '_Image__width': 10,
                #  '_Image__height': 10,
                #  '_Image__colors': {'#FFFFFF'}}
                return self.__dict__[f'_{classname}__{name}']
            raise AttributeError(f"'{classname}' object has no attribute {name}")
    else:
        @property
        def background(self):
            return self.__background

        @property
        def width(self):
            return self.__width

        @property
        def height(self):
            return self.__height

        @property
        def colors(self):
            return set(self.__colors)


if __name__ == '__main__':
    ord = Ord()
    print(ord.a)  # 97
    print(ord.Z)  # 90

    const = Const()
    const.limit = 591
    print(const.limit)
    # const.limit = 1  # ValueError: cannot change a const attribute
    # del const.limit  # ValueError: cannot delete a const attribute

    Const = collections.namedtuple('_', 'min max')(191, 591)  # throwaway name for the named tuple
    print(Const.min, Const.max)
    Offset = collections.namedtuple('_', 'id name description')(*range(3))
    print(Offset.id, Offset.name, Offset.description)

    image = Image(10, 10)
    print(image.__dict__)
    print(image.colors)
    print(image.height)
    # print(image.__background)  # AttributeError: 'Image' object has no attribute '__background'
