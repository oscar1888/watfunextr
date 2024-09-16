from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode, Node


def parse(tokens: list[Token]) -> Node:
    current_tree = ListNode('Program')
    parent_stack: list = []

    for token in tokens:
        if token.token_type == TokenType.LPAR:
            parent_stack.append(current_tree)
            list_node = ListNode()
            current_tree.add_child(list_node)
            current_tree = list_node
        elif token.token_type == TokenType.RPAR:
            current_tree = parent_stack.pop()
        else:
            current_tree.add_child(token)

    return current_tree
