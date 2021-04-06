"""
[] [lightblue: Director]
//
[] [lightgreen: Secretary]
//
[Minion #1] [] [Minion #2]
"""

"""
[#00CCDE: MessageBox Window
    [lightgray: Frame
        [] [white: Message text]
        //
        [goldenrod: OK Button] [] [#ff0505: Cancel Button]
        /
        []
    ] 
]
"""

"""
BNF

    BLOCKS  ::= NODES+
    NODES   ::= NEW_ROW* NODE+
    NODE    ::= '[' (COLOR ':')? NAME? NODES* ']'
    COLOR   ::= '#'[\dA-Fa-f]{6} | [a-zA-Z]\w*
    NAME    ::= [^][/]+
    NEW_ROW ::= '/'
"""

__all__ = ['Block', 'get_root_block', 'get_empty_block', 'get_new_row', 'is_new_row']


class Block:
    def __init__(self, name, color='white'):
        self.name = name
        self.color = color
        self.children = []

    def has_children(self):
        return bool(self.children)

    def __str__(self):
        blocks = []
        if self.name is not None:
            color = f'{self.color}' if self.color else ""
            block = f'[{color}{self.name}'
            blocks.append(block)
        if self.children:
            blocks.append('\n')
            for block in self.children:
                if is_new_row(block):
                    blocks.append('/\n')
                else:
                    blocks.append(str(block))
        if self.name is not None:
            blocks[-1] += ']\n'
        return ''.join(blocks)


get_root_block = lambda: Block(None, None)
get_empty_block = lambda: Block('')
get_new_row = lambda: None
is_new_row = lambda x: x is None
