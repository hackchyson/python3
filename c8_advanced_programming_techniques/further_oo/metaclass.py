import collections


class SortedList:
    pass


collections.abc.Sequence.register(SortedList)


class LoadableSavable(type):
    def __init__(cls, classname, bases, dictionary):
        super().__init__(classname, bases, dictionary)

        assert (
                hasattr(cls, 'load') and
                isinstance(getattr(cls, 'load'), collections.abc.Callable)
        ), "class '" + classname + "' must provide a load() method"
        assert (
                hasattr(cls, 'save') and
                isinstance(getattr(cls, 'save'), collections.abc.Callable)
        ), "class '" + classname + "' must provide a save() method"


# modifying properties
class AutoSlotProperties(type):
    def __new__(mcl, classname, bases, dictionary):
        slots = list(dictionary.get('__slot__', []))  # get slots
        for getter_name in [key for key in dictionary if key.startswith('get_')]:
            if isinstance(dictionary[getter_name], collections.abc.Callable):
                name = getter_name[4:]
                slots.append('__' + name)  # alter slots
                getter = dictionary.pop(getter_name)
                setter_name = 'set_' + name
                setter = dictionary.get(setter_name, None)
                if setter is not None and isinstance(setter, collections.abc.Callable):
                    del dictionary[setter_name]
                dictionary[name] = property(getter, setter)  # convert to property
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


    g = Good()

    product = Product('111', '8mm Stapler')
    print(product.barcode, product.description)  # 111 8mm Stapler
    product.description = '8mm Stapler (long)'
    print(product.barcode, product.description)  # 111 8mm Stapler (long)

    print(product.__slots__)  # ('__barcode', '__description')

    for i in dir(product):
        print(i)
    # _Product__barcode
    # _Product__description
    # __class__
    # __delattr__
    # __dir__
    # __doc__
    # __eq__
    # __format__
    # __ge__
    # __getattribute__
    # __gt__
    # __hash__
    # __init__
    # __init_subclass__
    # __le__
    # __lt__
    # __module__
    # __ne__
    # __new__
    # __reduce__
    # __reduce_ex__
    # __repr__
    # __setattr__
    # __sizeof__
    # __slots__
    # __str__
    # __subclasshook__
    # barcode
    # description
