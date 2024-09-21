from watfunextr.parser.pt_validator import validate
from watfunextr.parser.parser_error import ParserError
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode, Node
from watfunextr.parser.parser_error import _format_unexpected_token as unexp_fmt


def parse(tokens: list[Token]) -> Node:
    if not tokens:
        raise ValueError('The program must include at least one token')
    if tokens[0].token_type != TokenType.LPAR:
        raise ParserError(unexp_fmt(tokens[0]))
    module_tree = ([], tokens[0].line, tokens[0].col)
    open_par_stack: list = [module_tree]

    for i, token in enumerate(tokens[1:]):
        if token.token_type not in {TokenType.LPAR, TokenType.RPAR}:
            open_par_stack[-1][0].append(token)
            continue
        if not open_par_stack[-1][0]:
            raise ParserError(unexp_fmt(token))
        if token.token_type == TokenType.LPAR:
            list_node = ([], token.line, token.col)
            open_par_stack[-1][0].append(list_node)
            open_par_stack.append(list_node)
        elif token.token_type == TokenType.RPAR:
            popped = open_par_stack.pop()
            if not open_par_stack:
                if i < len(tokens[1:]) - 1:
                    raise ParserError(unexp_fmt(tokens[1:][i + 1]))
                module_tree = ListNode(popped[1], popped[2], token.line, token.col, 'List', *popped[0])
            else:
                open_par_stack[-1][0][-1] = ListNode(popped[1], popped[2], token.line, token.col, 'List', *popped[0])

    if open_par_stack:
        raise ParserError(f'Syntax error: there {"are" if len(open_par_stack) > 1 else "is"} {len(open_par_stack)} unclosed parenthesis')

    validate(module_tree)

    return module_tree
