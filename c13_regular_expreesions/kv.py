#!/usr/bin/env python3
"""
@project: python3
@file: kv
@author: mike
@time: 2021/3/1
 
@function:
"""
import re

r'''^[ \t]*(?P<key>\w+)[ \t]*=[ \t]*(?P<value>[^\n]+)(?<![ \t])'''

r"""
^[ \t]*              # start of lien and optional leading whitespace
(?P<key>\w+)         # the key text
[ \t]*=[ \t]*        # the equals with optional surrounding whitespace
(?P<value>[^\n]+)    # the value text
(?<![ \t])           # negative lookbehind to avoid trailing whitespace
"""

text = '''\
Helen Patricia Sharman
Jim Sharman
Sharman Joshi
Helen Kelly
Helen
Helen P.
'''
r'''
\b(Helen      # word boundary + Helen
(?:\s+        # whitespace without capture
(?:P\.|Patricia))?)        # no capture, P. or Patricia, nongreedily
\s+           # whitespace
(?=Sharman\b) # look lookahead Sharman + word boundary
'''

r'''
(
(["'])            # "'
([^\1>]+?)        # non match quote or > 
\1
|
([^"' >]+)
)
'''


r'''
<img\s+                              # start of the tag
[^>]*?                               # any attributes that precede the src
src=                                 # start of the src attribute
(?:
     (?P<quote>["'])                 # opening quote
     (?P<qimage>[^\1>]+?)            # image filename
     (?P=quote)                      # closing quote matching the opening quote
|
     (?P<uimage>[^"' >]+             # unquoted image filename
)
[^>]*?                               # any attribute that follow the src
>     
'''
