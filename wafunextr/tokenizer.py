from wafunextr.token import Token
import re
from wafunextr.token_patterns import token_patterns
from wafunextr.token_type import TokenType


def _to_skip(token_type: TokenType, skip_ws: bool, skip_comments: bool) -> bool:
    return skip_ws and token_type == TokenType.WHITESPACE or skip_comments and token_type == TokenType.COMMENT


def tokenize(text: str, skip_ws: bool = True, skip_comments: bool = True) -> list[Token]:
    regex = '|'.join(f'(?P<{token_type.name}>{pattern})' for token_type, pattern in token_patterns.items())
    tokens_re = re.compile(regex, re.DOTALL)
    tokens = list(
        Token(getattr(TokenType, token_type), value)
        for match in tokens_re.finditer(text) for token_type, value in match.groupdict().items()
        if value and not _to_skip(getattr(TokenType, token_type), skip_ws, skip_comments)
    )
    return tokens
