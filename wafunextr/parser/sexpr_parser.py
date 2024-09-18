from wafunextr.parser.pt_validator import _validate
from wafunextr.parser.parser_error import ParserError
from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode, Node
from wafunextr.parser.parser_error import _format_unexpected_token as unexp_fmt


def parse(tokens: list[Token]) -> Node:
    if not tokens:
        raise ValueError('The program must include at least one token')
    if tokens[0].token_type != TokenType.LPAR:
        raise ParserError(unexp_fmt(tokens[0]))
    module_tree = ListNode(tokens[0].line, tokens[0].col)
    open_par_stack: list = [module_tree]

    for i, token in enumerate(tokens[1:]):
        if token.token_type not in {TokenType.LPAR, TokenType.RPAR}:
            open_par_stack[-1].add_child(token)
            continue
        if not open_par_stack[-1].children:
            raise ParserError(unexp_fmt(token))
        if token.token_type == TokenType.LPAR:
            list_node = ListNode(token.line, token.col)
            open_par_stack[-1].add_child(list_node)
            open_par_stack.append(list_node)
        elif token.token_type == TokenType.RPAR:
            popped: ListNode = open_par_stack.pop()
            popped.end_line = token.line
            popped.end_col = token.col
            if not open_par_stack and i < len(tokens[1:]) - 1:
                raise ParserError(unexp_fmt(tokens[1:][i + 1]))

    if open_par_stack:
        raise ParserError(f'Syntax error: there {"are" if len(open_par_stack) > 1 else "is"} {len(open_par_stack)} unclosed parenthesis')

    _validate(module_tree)

    return module_tree
