# coding=utf8
"""
@project: python3
@file: csv2html
@author: mike
@time: 2021/1/20
 
@function:
"""


def extract_fields(line):
    fields = []
    field = ''
    quote = None
    for c in line:
        if c in '"\'':  # string delimiter
            if quote is None:  # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c  # other quote inside quoted string
            continue
        if quote is None and c == ',':  # end of a field
            fields.append(field)
            field = ''
        else:
            field += c  # accumulating a field
    if field:
        fields.append(field)  # adding the last field
    return fields
