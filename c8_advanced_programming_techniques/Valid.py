import re
import numbers


class GenericDescriptor:
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.getter(instance)

    def __set__(self, instance, value):
        return self.setter(instance, value)


def valid_string(attr_name, empty_allowed=True, regex=None, acceptable=None):
    # class decorator
    # This decorator adds two attributes to the class it decorates:
    # a private data attribute and a descriptor.
    def decorator(cls):
        name = '__' + attr_name

        def getter(self):
            return getattr(self, name)

        def setter(self, value):
            assert isinstance(value, str), (attr_name + ' must be a string')
            if not empty_allowed and not value:
                raise ValueError('{} may not be empty'.format(attr_name))
            if ((acceptable is not None and value not in acceptable) or
                    (regex is not None and not regex.match(value))):
                raise ValueError('{attr_name} can not be set to {value}'.format(**locals()))
            setattr(self, name, value)

        setattr(cls, attr_name, GenericDescriptor(getter, setter))
        return cls

    return decorator


def valid_number(attr_name, minimum=None, maximum=None,
                 acceptable=None):
    def decorator(cls):
        name = "__" + attr_name

        def getter(self):
            return getattr(self, name)

        def setter(self, value):
            assert isinstance(value, numbers.Number), (
                    attr_name + " must be a number")
            if minimum is not None and value < minimum:
                raise ValueError("{attr_name} {value} is too small"
                                 .format(**locals()))
            if maximum is not None and value > maximum:
                raise ValueError("{attr_name} {value} is too big"
                                 .format(**locals()))
            if acceptable is not None and value not in acceptable:
                raise ValueError("{attr_name} {value} is unacceptable"
                                 .format(**locals()))
            setattr(self, name, value)

        setattr(cls, attr_name, GenericDescriptor(getter, setter))
        return cls

    return decorator


if __name__ == '__main__':
    @valid_string("name", empty_allowed=False)
    @valid_string("product_id", empty_allowed=False, regex=re.compile(r"[A-Z]{3}\d{4}"))
    @valid_string("category", empty_allowed=False,
                  acceptable=frozenset(["Consumables", "Hardware", "Software", "Media"]))
    @valid_number("price", minimum=0, maximum=1e6)
    @valid_number("quantity", minimum=1, maximum=1000)
    class StockItem:
        def __init__(self, name, product_id, category, price, quantity):
            self.name = name
            self.product_id = product_id
            self.category = category
            self.price = price
            self.quantity = quantity


    pc = StockItem("Computer", "EAA5000", "Hardware", 599, 3)
    # pc.name=''
    # pc.product_id='ABC'
    # pc.category = 'Software ha'
