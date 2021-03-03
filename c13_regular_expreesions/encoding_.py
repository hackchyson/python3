#!/usr/bin/env python3
"""
@project: python3
@file: encoding_
@author: mike
@time: 2021/3/3
 
@function:
"""
import re

binary = b''

re_binary = r"""
# A lookbehind assertion that says that the
# match cannot be preceded by a hyphen or a word character.
(?<![-\w]) 
(?:(?:en)?coding|charset)  # encoding|coding|charset
(?:=(["'])?([-\w]+)(?(1)\1)
|:\s*([-\w]+))
""".encode('utf8')
match = re.search(re_binary, binary, re.IGNORECASE | re.VERBOSE)
encoding = match.group(match.lastindex) if match else b'utf8'

text = 'hello world'
re.split(r"\s+", text)
# same to
text.split()
