from typing import Union
from wafunextr.parser.parser_error import ParserError
from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode, Node
from wafunextr.parser.parser_error import _format_unexpected_token as unexp_fmt

val_type = {TokenType.NUM_TYPE}

var = {TokenType.NAT, TokenType.NAME}

ops = {
    TokenType.UNREACHABLE,
    TokenType.NOP,
    TokenType.BR,
    TokenType.BR_IF,
    TokenType.RETURN,
    TokenType.CALL,
    TokenType.DROP,
    TokenType.SELECT,
    TokenType.LOCAL_INSTR,
    TokenType.CONST_INSTR,
    TokenType.INT_INSTR,
    TokenType.FLOAT_INSTR,
    TokenType.GLOBAL_INSTR
}

expr_alts = {
    TokenType.BLOCK,
    TokenType.LOOP,
    TokenType.IF
}

instr_kw = ops | expr_alts


def children_left(index: int, pt: ListNode, require_zero=False, require_at_least_one=False):
    if require_zero and require_at_least_one:
        raise ValueError('Cannot require zero and one children at the same time')
    if not require_zero and not require_at_least_one:
        return index < len(pt.children)
    if require_zero:
        if index < len(pt.children):
            raise ParserError(unexp_fmt(pt.children[index]))
        return
    if index >= len(pt.children):
        raise ParserError(f"Syntax error at {pt.end_line}:{pt.end_col}: unexpected ')'")


def tokentype_set(token_type: Union[dict, set, TokenType]):
    if isinstance(token_type, dict):
        return set(token_type.keys())
    return token_type if isinstance(token_type, set) else {token_type}


def match_token(poss_token: Node, token_type: Union[dict, set, TokenType], opt=False):
    token_type = tokentype_set(token_type)
    if opt:
        return isinstance(poss_token, Token) and poss_token.token_type in token_type
    if not isinstance(poss_token, Token):
        raise ParserError(unexp_fmt(poss_token))
    if poss_token.token_type not in token_type:
        raise ParserError(unexp_fmt(poss_token))


def match_sexp(poss_sexp: Node, token_type: Union[dict, set, TokenType], opt=False):
    token_type = tokentype_set(token_type)
    if opt:
        return isinstance(poss_sexp, ListNode) and poss_sexp.children[0].token_type in token_type
    if not isinstance(poss_sexp, ListNode):
        raise ParserError(unexp_fmt(poss_sexp))
    if poss_sexp.children[0].token_type not in token_type:
        raise ParserError(unexp_fmt(poss_sexp.children[0]))


def is_next_child_a_token(index: int, pt: ListNode, token_type: Union[dict, set, TokenType]):
    return children_left(index, pt) and match_token(pt.children[index], token_type, opt=True)


def is_next_child_a_sexp(index: int, pt: ListNode, token_type: Union[dict, set, TokenType]):
    return children_left(index, pt) and match_sexp(pt.children[index], token_type, opt=True)


def match_zero_or_more_sexp(index: int, pt: ListNode, token_type: Union[dict, set, TokenType], sexp_func):
    while children_left(index, pt) and match_sexp(pt.children[index], token_type, opt=True):
        sexp_func(pt.children[index]) if not isinstance(sexp_func, dict) else sexp_func[pt.children[index].children[0].token_type](pt.children[index])
        pt.children[index].name = pt.children[index].children[0].token_type.name
        index += 1
    return index


def match_zero_or_more_token(index: int, pt: ListNode, token_type: Union[dict, set, TokenType]):
    while children_left(index, pt) and match_token(pt.children[index], token_type, opt=True):
        index += 1
    return index
