# Imagine that we have a class whose instances hold
# some strings. We want to access the strings in the normal way, for example,
# as a property, but we also want to get an XML-escaped version of the strings
# whenever we want.
import defusedxml


def fake_process(line):
    return 'processed: {}'.format(line)


# descriptors used to generate data without necessarily storing it
class XmlShadow:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    # instance is the Product instance
    # owner is the owning class (Product class)
    def __get__(self, instance, owner=None):
        # The XML modules are not secure against erroneous or maliciously constructed data.
        # If you need to parse untrusted or unauthenticated data see XML vulnerabilities.
        # return xml.sax.saxutils.escape(getattr(instance, self.attribute_name))
        return fake_process(getattr(instance, self.attribute_name))


# If the use case was that only a small proportion of the products were accessed
# for their XML strings, but the strings were often long and the same ones were
# frequently accessed, we could use a cache.
class CachedXmlShadow:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        self.cache = {}

    def __get__(self, instance, owner=None):
        xml_text = self.cache.get(id(instance))
        if xml_text is not None:
            return xml_text
        # The key is necessary because descriptors are created per class
        # rather than per instance.
        #         Insert key with a value of default if key is not in the dictionary.
        #         Return the value for key if key is in the dictionary, else default.
        # return self.cache.setdefault(id(instance), xml.sax.saxutils.escape(getattr(instance, self.attribute_name)))
        return self.cache.setdefault(id(instance), fake_process(getattr(instance, self.attribute_name)))


class Product:
    __slots__ = ('name', 'description', 'price')
    # The name_as_xml and description_as_xml class attributes are
    # set to be instances of the XmlShadow descriptor.

    name_as_xml = XmlShadow('name')
    description_as_xml = XmlShadow('description')

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


# descriptor that can be used to store all of an object’s at-
# tribute data, with the object not needing to store anything itself.
class ExternalStorage:
    __slots__ = ('attribute_name',)
    __storage = {}  # class attribute

    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def __set__(self, instance, value):
        self.__storage[id(instance), self.attribute_name] = value

    def __get__(self, instance, owner):
        # if we have p = Point(3, 4) , we can
        # access the x-coordinate with p.x , and we can access the ExternalStorage object
        # that holds all the x s with Point.x .
        if instance is None:
            return self
        return self.__storage[id(instance), self.attribute_name]

    def __str__(self):
        return str(self.__storage)


class Point:
    # By setting __slots__ to an empty tuple we ensure that the class cannot store
    # any data attributes at all.
    __slots__ = ()
    x = ExternalStorage('x')
    y = ExternalStorage('y')

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# self defined property
class Property:
    def __init__(self, getter, setter=None):
        self.__getter = getter
        self.__setter = setter
        self.__name__ = getter.__name__

    # At first sight,
    # self.__getter() looks like a method call, but it is not. In fact, self.__getter
    # is an attribute, one that happens to hold an object reference to a method
    # that was passed in. So what happens is that first we retrieve the attribute
    # ( self.__getter ), and then we call it as a function () . And because it is called as
    # a function rather than as a method we must pass in the relevant self object
    # explicitly ourselves.
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.__getter(instance)

    def __set__(self, instance, value):
        if self.__setter is None:
            raise AttributeError("'{}' is read-only".format(self.__name__))
        return self.__setter(instance, value)

    def setter(self, setter):
        self.__setter = setter
        return self.__setter


class NameAndExtension:

    def __init__(self, name, extension):
        self.__name = name
        self.extension = extension

    @Property
    def name(self):
        return self.__name

    @Property
    def extension(self):
        return self.__extension  # todo ?

    @extension.setter
    def extension(self, extension):
        self.__extension = extension


if __name__ == '__main__':
    # This works because when we try to access, for example, the name_as_xml
    # attribute, Python finds that the Product class has a descriptor with that name,
    # and so uses the descriptor to get the attribute’s value.

    product = Product("Chisel <3cm>", "Chisel & cap", 45.25)
    print(product.name, product.name_as_xml, product.description_as_xml)

    p = Point(3, 4)
    print(p.x, p.y)
    p = Point(1, 2)
    print(p.x, p.y)
    print(Point.x, Point.y, Point, sep='\n')
    # {(139973669757216, 'x'): 3, (139973669757216, 'y'): 4, (139973669757328, 'x'): 1, (139973669757328, 'y'): 2}
    # {(139973669757216, 'x'): 3, (139973669757216, 'y'): 4, (139973669757328, 'x'): 1, (139973669757328, 'y'): 2}
    # <class '__main__.Point'>

    print('=' * 100)
    ne = NameAndExtension('python', '.pdf')
    print(ne.name)
    print(ne.extension)
    print(ne.__dict__)
    ne.extension = '.tex'
