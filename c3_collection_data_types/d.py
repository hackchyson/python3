# coding=utf8
"""
@project: python3
@file: d
@author: mike
@time: 2021/1/22
 
@function:
"""

import os
import collections

# filename: filesize
d = {name: os.path.getsize(name) for name in os.listdir('.') if os.path.isfile(name)}
print(d)

# revert dict
inserted_d = {v: k for k, v in d.items()}
print(inserted_d)

d = collections.OrderedDict([('z', -4), ('e', 19), ('k', 7)])
for k in d:
    print(k, d[k])

tasks = collections.OrderedDict()
tasks[8031] = "Backup"
tasks[4027] = "Scan Email"
tasks[5733] = "Build System"
for k in tasks:
    print(k, tasks[k])
