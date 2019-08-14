import cProfile


def function_a(x, y):
    return x + y


def function_b(x, y):
    return x * y


def function_c(x, y):
    return x / y


X = 100
Y = 10

if __name__ == "__main__":
    for function in ('function_a', 'function_b', 'function_c'):
        cProfile.run('for i in range(10000000): {}(X,Y)'.format(function))

#          10000003 function calls in 1.687 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    1.246    1.246    1.687    1.687 <string>:1(<module>)
#  10000000    0.441    0.000    0.441    0.000 timeit_.py:4(function_a)
#         1    0.000    0.000    1.687    1.687 {built-in method builtins.exec}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#
#
#          10000003 function calls in 1.865 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    1.295    1.295    1.865    1.865 <string>:1(<module>)
#  10000000    0.570    0.000    0.570    0.000 timeit_.py:8(function_b)
#         1    0.000    0.000    1.865    1.865 {built-in method builtins.exec}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#
#
#          10000003 function calls in 1.815 seconds
#
#    Ordered by: standard name
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    1.332    1.332    1.815    1.815 <string>:1(<module>)
#  10000000    0.483    0.000    0.483    0.000 timeit_.py:12(function_c)
#         1    0.000    0.000    1.815    1.815 {built-in method builtins.exec}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


# ncalls: numbers of calls
# tottime: total time (excludes time spent inside functions called by the functions.)
# percall = tottime // ncalls (first percall)
# cumtime: cumulative time (includes time spent inside functions called by the functions.)
# percall = cumtime // ncalls (second percall)
