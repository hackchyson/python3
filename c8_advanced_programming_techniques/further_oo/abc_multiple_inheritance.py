import pickle
import abc
from c8_advanced_programming_techniques.further_oo.abc__Abstract import Undo


class LoadSave:
    def __init__(self, filename, *attribute_names):
        self.filename = filename
        self.__attribute_names = []
        for name in attribute_names:
            if name.startswith('__'):
                name = '_' + self.__class__.__name__ + name
            self.__attribute_names.append(name)

    def save(self):
        with open(self.filename, 'wb') as fh:
            data = []
            for name in self.__attribute_names:
                data.append(getattr(self, name))
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open(self.filename, 'rb') as fh:
            data = pickle.load(fh)
            for name, value in zip(self.__attribute_names, data):
                setattr(self, name, value)


class FileStack(Undo, LoadSave):
    def __init__(self, filename):
        Undo.__init__(self)
        LoadSave.__init__(self, filename, '__stack')
        self.__stack = []

    def load(self):
        super().load()
        Undo.clear(self)

    # The following is same to Stack
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
        assert self.__stack, "Stack is empty"
        return self.__stack[-1]

    def __eq__(self, other):
        return self.__stack == other.__stack

    def __str__(self):
        return str(self.__stack)
