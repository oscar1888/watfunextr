from wafunextr.tokenizer.token import Token
from wafunextr.utils import Node


def _format_unexpected_token(node: Node):
    return f"Syntax error at {node.line}:{node.col}: unexpected {repr(node.token_value) if isinstance(node, Token) else repr('(')}"


def _format_expected_token(end_line: int, end_col: int, token_name: str):
    return f'Syntax error at {end_line}:{end_col}: expecting {str(token_name)}'


class ParserError(Exception):
    pass
