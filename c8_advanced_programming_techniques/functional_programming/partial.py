# Partial function application is the creation of a function from an existing
# function and some arguments to produce a new function that does what the
# original function did, but with some arguments fixed so that callers don’t have
# to pass them.
import functools
from keras.layers import Conv2D, Input
from keras.regularizers import l2

lines = list('abcdefg')
import tkinter


def process_line(i, line):
    print(i, line)


# useful
enumerate1 = functools.partial(enumerate, start=1)
for lino, line in enumerate1(lines):
    process_line(lino, line)

reader = functools.partial(open, mode='rt', encoding='utf8')
writer = functools.partial(open, mode='wt', encoding='utf8')

l2_reg = 0.0
input_layer = Input((None, None, 3))

Conv2D_ = functools.partial(Conv2D, kernel_size=(3, 3), activation='relu', padding='same')

h = Conv2D_(256)(input_layer)
h = Conv2D_(64)(h)

# The same full code is:
# h = Conv2D(256, (3, 3), activation='relu', padding='same')(input_layer)
# h = Conv2D(64, (3, 3), activation='relu', padding='same')(h)
