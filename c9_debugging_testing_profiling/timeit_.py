import timeit


def function_a(x, y):
    return x + y


def function_b(x, y):
    return x * y


def function_c(x, y):
    return x / y


X = 100
Y = 10

if __name__ == "__main__":
    repeats = 10000000
    for function in ("function_a", "function_b", "function_c"):
        t = timeit.Timer("{0}(X, Y)".format(function),  # the code we want to execute and time
                         "from __main__ import {0}, X, Y".format(function))  # import from this model
        sec = t.timeit(repeats)  # default, 1 million repeats
        print("{function}() {sec:.6f} sec".format(**locals()))

# function_a() 0.495865 sec
# function_b() 0.601726 sec
# function_c() 0.550583 sec
