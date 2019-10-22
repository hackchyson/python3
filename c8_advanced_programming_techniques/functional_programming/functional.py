import functools
import operator
import os
import itertools
import numpy as np

# map
lst = [1, 2, 3, 4]
print(list(map(lambda x: x ** 2, lst)))  # map

print([x ** 2 for x in lst])  # list comprehension
print(list(x ** 2 for x in lst))  # generator

# filter
print(list(filter(lambda x: x > 0, [1, -1, 2, -2])))
print([x for x in [1, -1, 2, -1] if x > 0])

print(functools.reduce(lambda x, y: x * y, lst))
print(functools.reduce(operator.mul, lst))
# The operator module has functions for all of Python’s operators specifically to
# make functional-style programming easier.

files = os.listdir('.')
print(files)
total_size = functools.reduce(operator.add, (os.path.getsize(x) for x in files))
print(total_size)
total_size = functools.reduce(operator.add, map(os.path.getsize, files))
print(total_size)

filtered_total_size = functools.reduce(operator.add, map(os.path.getsize, filter(lambda x: x.endswith('.py'), files)))
print(filtered_total_size)
filtered_total_size = functools.reduce(operator.add, map(os.path.getsize, (x for x in files if x.endswith('.py'))))
print(filtered_total_size)
filtered_total_size = functools.reduce(operator.add, (os.path.getsize(x) for x in files if x.endswith('.py')))
print(filtered_total_size)
filtered_total_size = sum(os.path.getsize(x) for x in files if x.endswith('.py'))
print(filtered_total_size)


# Whereas slicing can be used to extract a sequence of part of a list, and slicing
# with striding can be used to extract a sequence of parts (say, every third item
# with L[::3] ), operator.itemgetter() can be used to extract a sequence of arbi-
# trary parts, for example, operator.itemgetter(4, 5, 6, 11, 18)(L) .

class Node:
    def __init__(self, priority):
        self.priority = priority

    def __str__(self):
        return str(self.priority)


# When we want to sort we can specify a key function. This function can be any
# function, for example, a lambda function, a built-in function or method (such
# as str.lower() ), or a function returned by operator.attrgetter() .
L = []
for i in [8, 5, 0, 2, 3, -1, 29]:
    L.append(Node(i))
L.sort(key=operator.attrgetter('priority'))
print([str(x) for x in L])

total = 0
# The itertools.chain() function returns an iterator that gives successive values
# from the first sequence it is given, then successive values from the second
# sequence, and so on until all the values from all the sequences are used.
for value in itertools.chain(np.arange(0, 10), np.arange(11, 20), np.arange(21, 30)):
    total += value
print(total)
