"""
Handcraft parse Block format.
"""
import Block

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


class LexError(Exception):
    pass


class Data:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.brackets = 0
        self.stack = [Block.get_root_block()]

    def location(self):
        return f'line {self.line}, column {self.column}'

    def advance_by(self, amount):
        for x in range(amount):
            self._advance_by_one()

    def _advance_by_one(self):
        self.pos += 1
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column += 1
        else:
            self.column += 1

    def advance_to_position(self, position):
        while self.pos < position:
            self._advance_by_one()

    def advance_up_to(self, characters):
        """
        Advance over whitespace until the character at the current position is
        one of those in the given string of characters.

        :param characters:
        :return:
        """
        while self.pos < len(self.text) and self.text[self.pos] not in characters and self.text[self.pos].isspace():
            self._advance_by_one()

        if not self.pos < len(self.text):
            return False
        if self.text[self.pos] in characters:
            return True
        raise LexError(f'expected {characters} but got {self.text[self.pos]}')


def recursive_descent_parse(text):
    def parse_block_data(data, end):
        color = None
        colon = data.text.find(':', data.pos)
        if -1 < colon < end:
            color = data.text[data.pos:colon]
            data.advance_to_position(colon + 1)

        name = data.text[data.pos:end].strip()
        data.advance_to_position(end)
        if not name and color is None:
            block = Block.get_empty_block()
        else:
            block = Block.Block(name, color)
        data.stack[-1].children.append(block)
        return block

    def parse_block(data):
        data.advance_by(1)
        next_block = data.text.find('[', data.pos)
        end_of_block = data.text.find(']', data.pos)
        if next_block == -1 or end_of_block < next_block:
            parse_block_data(data, end_of_block)
        else:
            block = parse_block_data(data, next_block)
            data.stack.append(block)
            parse(data)
            data.stack.pop()

    def parse_new_row(data):
        data.stack[-1].children.append(Block.get_new_row())
        data.advance_by(1)

    def parse(data):
        while data.pos < len(data.text):
            if not data.advance_up_to('[]/'):
                break
            if data.text[data.pos] == '[':
                data.brackets += 1
                parse_block(data)
            elif data.text[data.pos] == '/':
                parse_new_row(data)
            elif data.text[data.pos] == ']':
                data.brackets -= 1
                data.advance_by(1)
            else:
                raise LexError(f"expected '[', ']', or '/'; but got {data.text[data.pos]}")

    data = Data(text)
    try:
        parse(data)
    except LexError as err:
        raise ValueError('Error {{0}}:{0}: {1}'.format(data.location(), err))

    return data.stack[0]
