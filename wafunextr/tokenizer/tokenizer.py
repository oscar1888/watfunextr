from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_patterns import token_patterns
from wafunextr.tokenizer.token_type import TokenType
import re

from wafunextr.tokenizer.tokenizer_error import TokenizerError


def _to_skip(token_type: TokenType, skip_ws: bool, skip_comments: bool) -> bool:
    return skip_ws and token_type == TokenType.WHITESPACE or skip_comments and token_type == TokenType.COMMENT


def tokenize(text: str, skip_ws: bool = True, skip_comments: bool = True) -> list[Token]:
    regex = '|'.join(f'(?P<{token_type.name}>{pattern})' for token_type, pattern in token_patterns.items())
    tokens_re = re.compile(regex, re.DOTALL)

    tokens = []
    line = 1
    recognized_index = 0
    for match in tokens_re.finditer(text):
        token_type, value = list(filter(lambda e: e[1] is not None, match.groupdict().items()))[0]
        if match.start() != recognized_index:
            raise TokenizerError(f'Unexpected token at line {line}: {text[recognized_index:match.start()]}')
        recognized_index = match.end()
        token_type = getattr(TokenType, token_type)
        if not _to_skip(token_type, skip_ws, skip_comments): tokens.append(Token(token_type, value, line))
        line += value.count('\n')

    if recognized_index != len(text):
        raise TokenizerError(f'Unexpected token at line {line}: {text[recognized_index:len(text)]}')


    return tokens
