from wafunextr.parser.parser_error import ParserError
from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode, Node


def parse(tokens: list[Token]) -> Node:
    if not tokens:
        raise ValueError('The program must include at least one token')
    current_tree = ListNode('Program')
    parent_stack: list = []

    for token in tokens:
        if token.token_type == TokenType.LPAR:
            parent_stack.append(current_tree)
            list_node = ListNode()
            current_tree.add_child(list_node)
            current_tree = list_node
        elif token.token_type == TokenType.RPAR:
            if not parent_stack:
                raise ParserError(f'Syntax error at {token.line}:{token.col}: unexpected right parenthesis')
            if not current_tree.children:
                raise ParserError(f'Syntax error at {token.line}:{token.col}: empty parenthesis')
            current_tree = parent_stack.pop()
        else:
            current_tree.add_child(token)

    if parent_stack:
        raise ParserError(f'Syntax error: there {"are" if len(parent_stack) > 1 else "is"} {len(parent_stack)} unclosed parenthesis')

    return current_tree
