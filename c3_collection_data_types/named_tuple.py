# coding=utf8
"""
@project: python3
@file: named_tuple
@author: mike
@time: 2021/1/20
 
@function:
"""

import collections

Fullname = collections.namedtuple('Fullname',
                                  'firstname middlename lastname')
persons = []
persons.append(Fullname('Mike', 'Ming', 'Chyson'))
persons.append(Fullname('Alfred', 'Bernhard', 'Nobel'))
for person in persons:
    print('{firstname} {middlename} {lastname}'.format(**person._asdict()))
