from wafunextr.tokenizer.token_type import TokenType


class Token:

    def __init__(self, token_type: TokenType, token_value: str, line: int, col: int):
        if token_value == '':
            raise ValueError('The token value cannot be empty')
        if line < 1:
            raise ValueError('The line cannot be less than 1')
        if col < 1:
            raise ValueError('The column cannot be less than 1')
        self.token_type = token_type
        self.token_value = token_value
        self.line = line
        self.col = col

    def __repr__(self):
        return f'({self.token_type}, {repr(self.token_value)}, {self.line}:{self.col})'

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.token_type, self.token_value, self.line, self.col) == (other.token_type, other.token_value, other.line, other.col)
        raise NotImplemented
