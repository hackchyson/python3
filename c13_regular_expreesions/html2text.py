#!/usr/bin/env python3
"""
@project: python3
@file: html2text
@author: mike
@time: 2021/3/2
 
@function:

"""
import html
import re


def html2text(html_text):
    def char_from_entity(match):
        code = html.entities.name2codepoint.get(match.group(1), 0xFFFD)
        return chr(code)

    # (?s) math . include newline
    text = re.sub(r"(?s)<!--.*?-->", "", html_text)  # HTML comments
    text = re.sub(r"<[Pp][^>]*?>", '\n\n', text)  # opening paragraph tags
    text = re.sub(r"<[^>]*?>", '', text)  # any tag
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)  # &#165; for ¥
    text = re.sub(r"&([A-Za-z]+);", char_from_entity, text)  # named entities
    text = re.sub(r"\n(?:[ \xA0\t]+\n)+", '\n', text)  # linesthat contain only whitespace
    # Replace sequences of two or more newlines with exactly two newlines
    text = re.sub(r"\n\n+", '\n\n', text.strip())
    return text
