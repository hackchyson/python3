# coding=utf8
"""
@project: python3
@file: base64_
@author: mike
@time: 2021/2/4
 
@function:
"""
import base64

binary = open('ali.png', 'rb').read()
ascii_text = ''
for i, c in enumerate(base64.b64encode(binary)):
    if i and i % 68 == 0:
        ascii_text += '\\\n'
    ascii_text += chr(c)
print(ascii_text)

binary = base64.b64decode(ascii_text)
open('ali_copy.png', 'wb').write(binary)
