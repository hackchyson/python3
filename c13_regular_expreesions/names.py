#!/usr/bin/env python3
"""
@project: python3
@file: names
@author: mike
@time: 2021/3/2
 
@function:
"""
import re

# from Forename Middlename1 ... MiddlenameN Surname
# to Surname,ForenameMiddlename1...MiddlenameN
names = ['Mike Ming Chyson', 'Maël Ming Li']
new_names = []
for name in names:
    # name = re.sub(r"(\w+(?:\s+\w+)*)\s+(\w+)", r"\2, \1", name)
    name = re.sub(r"(?P<forenames>\w+(?:\s+\w+)*)"
                  r"\s+(?P<surname>\w+)",
                  r"\g<surname>, \g<forenames>",
                  name)
    new_names.append(name)
for name in new_names:
    print(name)
# Chyson, Mike Ming
# Li, Maël Ming
