from wafunextr.token_type import TokenType


class Token:

    def __init__(self, token_type: TokenType, token_value: str):
        if token_value == '':
            raise ValueError('The token value cannot be empty')
        self.token_type = token_type
        self.token_value = token_value

    def __repr__(self):
        return f'({self.token_type}, {repr(self.token_value)})'

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.token_type, self.token_value) == (other.token_type, other.token_value)
        raise NotImplemented
