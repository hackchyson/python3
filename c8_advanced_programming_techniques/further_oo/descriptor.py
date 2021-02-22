# Imagine that we have a class whose instances hold
# some strings. We want to access the strings in the normal way, for example,
# as a property, but we also want to get an XML-escaped version of the strings
# whenever we want.
import defusedxml
from xml.sax.saxutils import escape


class XmlShadow:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def __get__(self, instance, owner=None):
        return escape(getattr(instance, self.attribute_name))


class CachedXmlShadow:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        self.cache = {}

    def __get__(self, instance, owner=None):
        xml_text = self.cache.get(id(instance))
        if xml_text is not None:
            return xml_text
        return self.cache.setdefault(id(instance), escape(getattr(instance, self.attribute_name)))


class Product:
    __slots__ = ('__name', '__description', '__price')

    name_as_xml = XmlShadow('name')
    description_as_xml = XmlShadow('description')

    def __init__(self, name, description, price):
        self.__name = name
        self.__description = description
        self.__price = price

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price


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
        if instance is None:
            d = {}
            for k in self.__storage.keys():
                if self.attribute_name in k:
                    d[k] = self.__storage[k]
            return d
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


class Property:
    def __init__(self, getter, setter=None):
        self.__getter = getter
        self.__setter = setter
        self.__name__ = getter.__name__

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.__getter(instance)

    def __set__(self, instance, value):
        if self.__setter is None:
            raise AttributeError(f"'{self.__name__}' is read-only")
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
        return self.__extension

    @extension.setter
    def extension(self, extension):
        self.__extension = extension


if __name__ == '__main__':
    # This works because when we try to access, for example, the name_as_xml
    # attribute, Python finds that the Product class has a descriptor with that name,
    # and so uses the descriptor to get the attribute’s value.

    product = Product("Chisel <3cm>", "Chisel & cap", 45.25)
    print(product.name, product.name_as_xml, product.description_as_xml, sep='\n')
    # Chisel <3cm>
    # Chisel &lt;3cm&gt;
    # Chisel &amp; cap

    p = Point(3, 4)
    print(p.x, p.y)  # 3 4
    p = Point(1, 2)
    print(p.x, p.y)  # 1 2
    print(Point.x, Point.y, Point, sep='\n')
    # {(140338432304624, 'x'): 3, (140338432304640, 'x'): 1}
    # {(140338432304624, 'y'): 4, (140338432304640, 'y'): 2}
    # <class '__main__.Point'>

    print('=' * 100)
    ne = NameAndExtension('python', '.pdf')
    print(ne.name)
    print(ne.extension)
    print(ne.__dict__)
    ne.extension = '.tex'
