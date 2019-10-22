import collections


class SortedList:
    pass


# Registering a class like this makes it a virtual subclass. A virtual subclass
# reports that it is a subclass of the class or classes it is registered with (e.g.,
# using isinstance() or issubclass() ), but does not inherit any data or methods
# from any of the classes it is registered with.
collections.Sequence.register(SortedList)


# Suppose we want to create a group of classes that all provide load() and save()
# methods. We can do this by creating a class that when used as a metaclass,
# checks that these methods are present

# Classes that are to serve as metaclasses must inherit from the ultimate
# metaclass base class, type , or one of its subclasses.

# Note that this class is called when classes that use it are instantiated, in all
# probability not very often, so the runtime cost is extremely low.
class LoadableSavable(type):
    def __init__(cls, classname, bases, dictionary):
        super().__init__(classname, bases, dictionary)  # class instantiated

        # We could have checked that the load and save attributes are callable using
        # hasattr() to check that they have the __call__ attribute, but we prefer to
        # check whether they are instances of collections.Callable instead. The collec-
        # tions.Callable abstract base class provides the promise (but no guarantee) that
        # instances of its subclasses (or virtual subclasses) are callable.
        assert hasattr(cls, 'load') and isinstance(getattr(cls, 'load'), collections.Callable), (
                "class '" + classname + "' must provide a load() method")
        assert hasattr(cls, 'save') and isinstance(getattr(cls, 'save'), collections.Callable), (
                "class '" + classname + "' must provide a save() method")


# modifying properties
class AutoSlotProperties(type):
    # We must use a reimplementation of __new__() rather than __init__()
    # because we want to change the dictionary before the class is created.
    def __new__(mcl, classname, bases, dictionary):
        slots = list(dictionary.get('__slot__', []))
        for getter_name in [key for key in dictionary if key.startswith('get_')]:
            if isinstance(dictionary[getter_name], collections.Callable):
                name = getter_name[4:]  # get_
                slots.append('__' + name)
                getter = dictionary.pop(getter_name)
                setter_name = 'set_' + name
                setter = dictionary.get(setter_name, None)
                if setter is not None and isinstance(setter, collections.Callable):
                    del dictionary[setter_name]
                dictionary[name] = property(getter, setter)
        dictionary['__slots__'] = tuple(slots)
        return super().__new__(mcl, classname, bases, dictionary)


class Product(metaclass=AutoSlotProperties):
    def __init__(self, barcode, description):
        self.__barcode = barcode
        self.description = description

    def get_barcode(self):
        return self.__barcode

    def get_description(self):
        return self.__description

    def set_description(self, description):
        if description is None or len(description) < 3:
            self.__description = '<Invalid Description>'
        else:
            self.__description = description


if __name__ == '__main__':
    # class Bad(metaclass=LoadableSavable):
    #     def some_method(self): pass
    # AssertionError: class 'Bad' must provide a load() method

    class Good(metaclass=LoadableSavable):
        def load(self): pass

        def save(self): pass


    product = Product('111', 'aaa')
    print(dir(product))
    print(product.barcode, product.description)
    product.description = '8mm Stapler (long)'
    print(product.barcode, product.description)

# Metaclasses are the last tool to reach for rather than the first, ex-
# cept perhaps for application framework developers who need to provide power-
# ful facilities to their users without making the users go through hoops to realize
# the benefits on offer.
