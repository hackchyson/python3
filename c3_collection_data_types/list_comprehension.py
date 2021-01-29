# coding=utf8
"""
@project: python3
@file: list_comprehension
@author: mike
@time: 2021/1/21
 
@function:
"""

codes = [s + z + c for s in "MF" for z in "SMLX" for c in "BGW" if not (s == "F" and z == "X")]
print(codes)

codes = []
for sex in "MF":  # Male, Female
    for size in "SMLX":  # Small, Medium, Large, eXtra large
        if sex == "F" and size == "X":
            continue
        for color in "BGW":  # Black, Gray, White
            codes.append(sex + size + color)
print(codes)
