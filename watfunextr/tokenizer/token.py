from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import Node


class Token(Node):

    def __init__(self, token_type: TokenType, token_value: str, line: int, col: int):
        super().__init__(line, col)
        if token_value == '':
            raise ValueError('The token value cannot be empty')
        self.token_type = token_type
        self.token_value = token_value

    def __repr__(self):
        return f'({self.token_type}, {repr(self.token_value)}, {self.line}:{self.col})'

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.token_type, self.token_value, self.line, self.col) == (other.token_type, other.token_value, other.line, other.col)
        raise NotImplemented
