import copy


def process(line):
    return line


filename = 'hello'

# without context manager
fh = None
try:
    fh = open(filename)
    for line in fh:
        process(line)
except EnvironmentError as err:
    print(err)
finally:
    if fh is not None:
        fh.close()

# with context manager
try:
    with open(filename) as fh:
        for line in fh:
            process(line)
except EnvironmentError as err:
    print(err)

source = 'hello'
target = 'world'

try:
    with open(source) as fin:
        with open(target, 'w') as fout:
            for line in fin:
                fout.write(process(line))
except EnvironmentError as err:
    print(err)

try:
    with open(source) as fin, open(target, 'w') as fout:
        for line in fin:
            fout.write(process(line))
except EnvironmentError as err:
    print(err)


# Suppose we want to perform several operations on a list in an atomic
# manner—that is, we either want all the operations to be done or none of them
# so that the resultant list is always in a known state.
class AtomicList:
    def __init__(self, alist, shallow_copy=True):
        self.original = alist
        self.shallow_copy = shallow_copy

    def __enter__(self):
        self.modified = (self.original[:] if self.shallow_copy else copy.deepcopy(self.original))
        return self.modified

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # exception type
            self.original[:] = self.modified


items = list(range(10))
index = 5
try:
    with AtomicList(items) as atomic:
        atomic.append(1111)
        del atomic[3]
        atomic[8] = 2222
        atomic[index] = 3333
except (AttributeError, IndexError, ValueError) as err:
    print('no changes applied:', err)
print(items)
