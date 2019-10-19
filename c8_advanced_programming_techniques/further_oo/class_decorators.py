from chyson.decorators.decorators import delegate, complete_comparisons

_identitiy = lambda x: x


@delegate('__list', ('pop', '__delitem__', '__getitem__', '__iter__', '__reversed__', '__len__', '__str__'))
class SortedList:
    def __init__(self, sequence=None, key=None):
        self.__key = key or _identitiy
        assert hasattr(self.__key, '__call__')
        if sequence is None:
            self.__list = []
        elif isinstance(sequence, SortedList) and sequence.key == self.__key:
            self.__list = sequence.__list[:]
        else:
            self.__list = sorted(list(sequence), key=self.__key)


@complete_comparisons
class FuzzyBool:
    def __init__(self, value=0.0):
        self.__value = value if 0.0 <= value <= 1.0 else 0.0

    def __lt__(self, other):
        return self.__value < other.__value

    def __repr__(self):
        return ("{0}({1})".format(self.__class__.__name__,
                                  self.__value))


if __name__ == '__main__':
    sl = SortedList([1, 2, 3])
    print(sl)
    print(sl.pop())
    print(len(sl))
    print(list(reversed(sl)))
    for i in sl:
        print(i)

    fb1 = FuzzyBool(0.5)
    fb2 = FuzzyBool(.7)
    print(fb1, fb2)
    print(fb1 < fb2, fb1 <= fb2, fb2 == fb2, fb1 != fb2, fb1 > fb2, fb1 >= fb2)
