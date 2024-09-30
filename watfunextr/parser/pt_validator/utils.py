from typing import Union
from watfunextr.parser.parser_error import ParserError
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode, Node

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

var_as_arg = {TokenType.BR, TokenType.BR_IF, TokenType.CALL, TokenType.LOCAL_INSTR, TokenType.GLOBAL_INSTR}

expr_token_names = {t.name for t in instr_kw}


def children_left(index: int, pt: ListNode, require_zero=False, require_at_least_one=False):
    if require_zero and require_at_least_one:
        raise ValueError('Cannot require zero and one children at the same time')
    if not require_zero and not require_at_least_one:
        return index < len(pt.children)
    if require_zero:
        if index < len(pt.children):
            raise ParserError(pt.children[index])
        return
    if index >= len(pt.children):
        raise ParserError(f"Unexpected ')'", line_col=(pt.end_line, pt.end_col))


def tokentype_set(token_type: Union[dict, set, TokenType]):
    if isinstance(token_type, dict):
        return set(token_type.keys())
    return token_type if isinstance(token_type, set) else {token_type}


def match_token(poss_token: Node, token_type: Union[dict, set, TokenType], opt=False):
    token_type = tokentype_set(token_type)
    if opt:
        return isinstance(poss_token, Token) and poss_token.token_type in token_type
    if not isinstance(poss_token, Token):
        raise ParserError(poss_token)
    if poss_token.token_type not in token_type:
        raise ParserError(poss_token)


def match_sexp(poss_sexp: Node, token_type: Union[dict, set, TokenType], opt=False):
    token_type = tokentype_set(token_type)
    if opt:
        return isinstance(poss_sexp, ListNode) and poss_sexp.children[0].token_type in token_type
    if not isinstance(poss_sexp, ListNode):
        raise ParserError(poss_sexp)
    if poss_sexp.children[0].token_type not in token_type:
        raise ParserError(poss_sexp.children[0])


def next_child_and_is_a_token(index: int, pt: ListNode, token_type: Union[dict, set, TokenType]):
    return children_left(index, pt) and match_token(pt.children[index], token_type, opt=True)


def next_child_and_is_a_sexp(index: int, pt: ListNode, token_type: Union[dict, set, TokenType]):
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


def match_zero_or_more_tokens_or_sexp_rule(index: int, pt: ListNode, token_type_token: Union[dict, set, TokenType], token_type_sexp: Union[dict, set, TokenType], token_func, sexp_func):
    while children_left(index, pt):
        if match_sexp(pt.children[index], token_type_sexp, opt=True):
            sexp_func(pt.children[index]) if not isinstance(sexp_func, dict) else sexp_func[pt.children[index].children[0].token_type](pt.children[index])
            pt.children[index].name = pt.children[index].children[0].token_type.name
        elif match_token(pt.children[index], token_type_token, opt=True):
            if token_func is not None:
                index = token_func(index, pt)
                continue
        else:
            break
        index += 1
    return index


def _op(index: int, pt: ListNode):
    match_token(pt.children[index], ops)

    if pt.children[index].token_type in var_as_arg:
        children_left(index+1, pt, require_at_least_one=True)
        match_token(pt.children[index+1], var)
        index += 1
    elif pt.children[index].token_type == TokenType.CONST_INSTR:
        children_left(index+1, pt, require_at_least_one=True)
        match_token(pt.children[index+1], {TokenType.NUM, TokenType.NAT})
        index += 1
    index += 1
    return index
