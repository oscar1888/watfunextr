from watfunextr.tokenizer.token import Token
from watfunextr.utils import Node


class ParserError(Exception):
    def __init__(self, msg_or_node, line_col=None):
        if isinstance(msg_or_node, Node):
            msg = f"Syntax error at {msg_or_node.line}:{msg_or_node.col}: unexpected {repr(msg_or_node.token_value) if isinstance(msg_or_node, Token) else repr('(')}"
        elif line_col is not None:
            msg = f'Syntax error at {line_col[0]}:{line_col[1]}: {msg_or_node}'
        else:
            msg = f'Syntax error: {msg_or_node}'
        super().__init__(msg)
