import cProfile
import math


def log(x, y):
    return math.log(x, y)


code = """
for i in range(10000):
    log(10, 2)
"""
cProfile.run(code)
