#!/usr/bin/env python3
"""
@project: python3
@file: generator
@author: mike
@time: 2021/2/7
 
@function:
"""
import sys
import os
import glob


def items_in_key_order(d):
    for key in sorted(d):
        yield key, d[key]  # yield


def items_in_key_order2(d):
    return ((key, d[key]) for key in sorted(d))  # generator expression


# def quarters(next_quarter=0.0):
#     while True:
#         yield next_quarter
#         next_quarter += 0.25
#
#
# result = []
# for x in quarters():
#     result.append(x)
#     if x >= 1.0:
#         break

def quarters(next_quarter=0.0):
    while True:
        received = (yield next_quarter)
        if received is None:
            next_quarter += 0.25
        else:
            next_quarter = received


result = []
generator = quarters()
while len(result) < 5:
    x = next(generator)
    if abs(x - 0.5) < sys.float_info.epsilon:
        x = generator.send(1.0)  # Notice this
    result.append(x)
print(result)  # [0.0, 0.25, 1.0, 1.25, 1.5]

if sys.platform.startswith('win'):
    def get_files(names):
        for name in names:
            if os.path.isfile(name):
                yield name
            else:
                for file in glob.iglob(name):
                    if not os.path.isfile(file):
                        continue
                    yield file
else:
    def get_files(names):
        return (file for file in names if os.path.isfile(file))
