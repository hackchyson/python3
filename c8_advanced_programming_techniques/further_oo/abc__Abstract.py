import abc


class Undo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.__undos = []

    @abc.abstractproperty
    def can_undo(self):
        return bool(self.__undos)

    @abc.abstractmethod
    def undo(self):
        assert self.__undos, 'nothing left to undo'
        # We must pass self because the method is being called as a function
        # and not as a method.
        self.__undos.pop()(self)

    def add_undo(self, undo):
        self.__undos.append(undo)


class Stack(Undo):
    def __init__(self):
        super().__init__()
        self.__stack = []

    @property
    def can_undo(self):
        return super().can_undo

    def undo(self):
        super().undo()

    def push(self, item):
        self.__stack.append(item)
        self.add_undo(lambda self: self.__stack.pop())

    def pop(self):
        item = self.__stack.pop()
        self.add_undo(lambda self: self.__stack.append(item))
        return item

    def top(self):
        assert self.__stack, 'Stack is empty'
        return self.__stack[-1]

    def __str__(self):
        return str(self.__stack)


if __name__ == '__main__':
    stack = Stack()
    for i in range(10):
        stack.push(i)
    print(stack)
    stack.pop()
    stack.pop()
    print(stack)
    print('=' * 100)
    for i in range(10):
        stack.undo()
        print(stack)
