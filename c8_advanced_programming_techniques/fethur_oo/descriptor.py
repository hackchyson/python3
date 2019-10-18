class Product:
    __slots__ = ('__name', '__description', '__price')
    name_as_xml = XmlShadow('name')
    description_as_xml = XmlShadow('description')

    def __init__(self, name, description, price):
        self.__name = name
        self.description = description
        self.price = price
