class TokenizerError(Exception):
    def __init__(self, msg):
        super().__init__(f'Lexer error: {msg}')
