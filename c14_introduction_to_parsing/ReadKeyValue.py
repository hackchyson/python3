import re

"""
[playlist]
File1=Blondie\Atomic\01-Atomic.ogg
Title1=Blondie - Atomic
Length1=230
...
File18=Blondie\Atomic\18-I'm Gonna Love You Too.ogg 
Title18=Blondie - I'm Gonna Love You Too 
Length18=-1
NumberOfEntries=18
Version=2
"""

"""
PLS ::= (LINE '\n')+
LINE ::= INI_HEADER | KEY_VALUE | COMMENT | BLANK 
INI_HEADER ::= '[' [^]]+ ']'
KEY_VALUE ::= KEY \s* '=' \s* VALUE?
KEY ::= \w+
VALUE ::= .+
COMMENT ::= #.*
BLANK ::= ^$
"""

INI_HEADER = re.compile(r"^\[[^]]+\]$")
KEY_VALUE_RE = re.compile(r"^(?P<key>\w+)\s*=\s*(?P<value>.*)$")


def dict_from_key_values(file, lowercase_keys=False):
    key_values = {}
    for lino, line in enumerate(file, start=1):
        line = line.strip()
        # Empty line or comment.
        if not line or line.startswith("#"):
            continue
        key_value = KEY_VALUE_RE.match(line)
        if key_value:
            key = key_value.group('key')
            if lowercase_keys:
                key = key.lower()
            key_values[key] = key_value.group('value')
        else:
            ini_header = INI_HEADER.match(line)
            if not ini_header:
                print(f'Failed to parse line {lino}: {line}')
    return key_values
