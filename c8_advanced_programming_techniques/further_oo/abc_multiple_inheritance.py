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


# This can be very convenient and works especially well when the inher-
# ited classes have no overlapping APIs.
class FileStack(Undo, LoadSave):
    def __init__(self, filename):
        # Instead of using super() in the __init__() method we must spec-
        # ify the base classes that we initialize since super() cannot guess our intentions.
        Undo.__init__(self)
        LoadSave.__init__(self, filename, '__stack')
        self.__stack = []

    def load(self):
        super().load()
        # for load() we must clear the undo stack after loading.
        # self.clear() # 1
        # super().clear() # 2
        Undo.clear(self)  # 3
