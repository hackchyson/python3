#!/usr/bin/env python3
"""
@project: python3
@file: re_
@author: mike
@time: 2021/3/1
 
@function:
"""
import re

# manner 1
text = '#C0C0AB'
match = re.search(r'#[\dA-Fa-f]{6}\b', text)

# manner 2
color_re = re.compile(r'#[\dA-Fa-f]{6}\b')
match = color_re.search(text)

# flag
match = re.search(r'#[\dA-F]{6}\b', text, re.IGNORECASE)
match = re.search(r'(?i)#[\dA-F]{6}\b', text)

text = 'win in vain'
text = "one and and two let's say"
double_word_re = re.compile(r"\b(?P<word>\w+)\s+(?P=word)(?!\w)", re.IGNORECASE)
double_word_re = re.compile(r"\b(?P<word>\w+)\s+(?P=word)\b", re.IGNORECASE)  # same to the above
for match in double_word_re.finditer(text):
    print(f'{match.group("word")} is duplicated')
# and is duplicated

text = '''
<img src="/images/stickman.gif" alt="Stickman" width="24" height="39">
<img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="32" height="32">
'''
image_re_text = r'''
<img\s+                              # start of the tag
[^>]*?                               # any attributes that precede the src
src=                                 # start of the src attribute
(?:
     (?P<quote>["'])                 # opening quote
     (?P<qimage>[^\1>]+?)            # image filename
     (?P=quote)                      # closing quote matching the opening quote
|
     (?P<uimage>[^"' >]+)            # unquoted image filename
)
[^>]*?                               # any attribute that follow the src
>     
'''
image_re = re.compile(image_re_text, re.IGNORECASE | re.VERBOSE)
image_files = []
for match in image_re.finditer(text):
    image_files.append(match.group("qimage") or match.group("uimage"))
for image_file in image_files:
    print(image_file)
# /images/stickman.gif
# https://www.w3schools.com/images/lamp.jpg
