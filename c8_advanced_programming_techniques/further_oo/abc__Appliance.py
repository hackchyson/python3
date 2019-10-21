import abc


# We have set the class’s metaclass to be abc.ABCMeta
# since this is a requirement for ABCs;
# any abc.ABCMeta subclass can be used instead, of course.
class Appliance(metaclass=abc.ABCMeta):
    # We have made __init__() an abstract method to ensure that it is reimplemented
    @abc.abstractmethod
    def __init__(self, model, price):
        self.__model = model
        self.price = price

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    # To make an abstract readable/writable property we cannot
    # use decorator syntax
    price = abc.abstractproperty(get_price, set_price)

    @property
    def model(self):
        return self.__model


class Cooker(Appliance):
    def __init__(self, model, price, fuel):
        super().__init__(model, price)
        self.fuel = fuel

    price = property(lambda self: super().price,
                     lambda self, price: super().set_price(price))


if __name__ == '__main__':
    # app = Appliance('r', 1) # TypeError: Can't instantiate abstract class Appliance with abstract methods __init__, price
    cooker = Cooker('r', 1, 'fuel')
    print(cooker.price)  # 1
