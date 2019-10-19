# Imagine that we have a class whose instances hold
# some strings. We want to access the strings in the normal way, for example,
# as a property, but we also want to get an XML-escaped version of the strings
# whenever we want.
import xml


class XmlShadow:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    # instance is the Product instance
    # owner is the owning class (Product class)
    def __get__(self, instance, owner=None):
        return xml.sax.saxutils.escape(getattr(instance, self.attribute_name))


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
        return self.cache.setdefault(id(instance), xml.sax.saxutils.escape(getattr(instance, self.attribute_name)))


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


if __name__ == '__main__':
    # This works because when we try to access, for example, the name_as_xml
    # attribute, Python finds that the Product class has a descriptor with that name,
    # and so uses the descriptor to get the attribute’s value.

    product = Product("Chisel <3cm>", "Chisel & cap", 45.25)
    print(product.name, product.name_as_xml, product.description_as_xml)
