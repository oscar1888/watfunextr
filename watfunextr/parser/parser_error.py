from watfunextr.tokenizer.token import Token
from watfunextr.utils import Node


class ParserError(Exception):
    def __init__(self, msg_or_node):
        if isinstance(msg_or_node, Node):
            msg = f"Syntax error at {msg_or_node.line}:{msg_or_node.col}: unexpected {repr(msg_or_node.token_value) if isinstance(msg_or_node, Token) else repr('(')}"
        else:
            msg = msg_or_node
        super().__init__(msg)
