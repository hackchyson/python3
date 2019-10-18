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
        # Shallow copying is fine for
        # lists of numbers or strings; but for lists that contain lists or other collections,
        # shallow copying is not sufficient.
        self.modified = (self.original[:] if self.shallow_copy else copy.deepcopy(self.original))
        return self.modified

    # The return value of __exit__() is used to indicate whether any exception that
    # occurred should be propagated. A True value means that we have handled any
    # exception and so no propagation should occur. Normally we always return
    # False or something that evaluates to False in a Boolean context to allow any
    # exception that occurred to propagate. By not giving an explicit return value,
    # our __exit__() returns None which evaluates to False and correctly causes any
    # exception to propagate.
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # exception type
            # We cannot do self.original = self.modified because that
            # would just replace one object reference with another and would not affect the
            # original list at all.
            self.original[:] = self.modified


try:
    items = list(range(10))
    index = 5
    with AtomicList(items) as atomic:
        atomic.append(1111)
        del atomic[3]
        atomic[8] = 2222
        atomic[index] = 3333
except (AttributeError, IndexError, ValueError) as err:
    print('no changes applied:', err)
print(items)
