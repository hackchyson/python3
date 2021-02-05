# coding=utf8
"""
@project: python3
@file: exec_
@author: mike
@time: 2021/2/5
 
@function:
"""

for i in range(3):
    exec(f'a{i} = {i}')
    exec(f'print(a{i})')
exec('me = "Mike Chyson"')
print(me)


exec('''
def say_hello():
    print('hello')
''')
say_hello()