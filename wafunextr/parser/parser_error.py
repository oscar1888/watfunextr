from wafunextr.tokenizer.token import Token
from wafunextr.utils import Node


def _format_unexpected_token(node: Node):
    return f"Syntax error at {node.line}:{node.col}: unexpected {repr(node.token_value) if isinstance(node, Token) else repr('(')}"


class ParserError(Exception):
    pass
