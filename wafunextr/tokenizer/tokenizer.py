from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_patterns import token_patterns
from wafunextr.tokenizer.token_type import TokenType
import re

from wafunextr.tokenizer.tokenizer_error import TokenizerError


def _find_match_group(match):
    return list(filter(lambda e: e[1] is not None, match.groupdict().items()))[0]


def _to_skip(token_type: TokenType, skip_ws: bool, skip_comments: bool) -> bool:
    return skip_ws and token_type == TokenType.WHITESPACE or skip_comments and token_type == TokenType.COMMENT


def tokenize(text: str, skip_ws: bool = True, skip_comments: bool = True) -> list[Token]:
    if not text:
        raise ValueError('WAT program cannot be empty')
    regex: str = '|'.join(f'(?P<{token_type.name}>{pattern})' for token_type, pattern in token_patterns.items())
    tokens_re = re.compile(regex, re.DOTALL)

    tokens: list[Token] = []
    line: int = 1
    recognized_index: int = 0
    last_newline_index: int = -1
    col: int = recognized_index - last_newline_index
    for match in tokens_re.finditer(text):
        token_type, value = _find_match_group(match)

        if match.start() != recognized_index:
            raise TokenizerError(
                f'Unexpected token at {line}:{col}: {text[recognized_index:match.start()]}')

        token_type = getattr(TokenType, token_type)
        if not _to_skip(token_type, skip_ws, skip_comments):
            tokens.append(Token(token_type, value, line, col))

        recognized_index = match.end()

        if token_type in {TokenType.WHITESPACE, TokenType.COMMENT}:
            line += value.count('\n')
            act_newline_index = value.rfind('\n')
            if act_newline_index != -1:
                last_newline_index = match.start() + act_newline_index

        col = recognized_index - last_newline_index

    if recognized_index != len(text):
        raise TokenizerError(
            f'Unexpected token at {line}:{col}: {text[recognized_index:len(text)]}')

    return tokens
