from wafunextr.parser.pt_validator.param_local_result import _result
from wafunextr.parser.pt_validator.utils import instr_kw, var, expr_alts, match_token, children_left, match_sexp, \
    is_next_child_a_token, match_zero_or_more_sexp, is_next_child_a_sexp
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode

var_as_arg = {TokenType.BR, TokenType.BR_IF, TokenType.CALL, TokenType.LOCAL_INSTR, TokenType.GLOBAL_INSTR}


def _block_loop_structure(pt: ListNode, token_type: TokenType):
    match_token(pt.children[0], token_type)

    index = 1
    if is_next_child_a_token(index, pt, TokenType.NAME):
        index += 1

    if is_next_child_a_sexp(index, pt, TokenType.RESULT):
        pt.children[index].name = pt.children[index].children[0].token_type.name
        index += 1

    index = match_zero_or_more_sexp(index, pt, instr_kw, _expr)

    children_left(index, pt, require_zero=True)


def _block_expr(pt: ListNode):
    _block_loop_structure(pt, TokenType.BLOCK)


def _loop_expr(pt: ListNode):
    _block_loop_structure(pt, TokenType.LOOP)


def _if_expr(pt: ListNode):
    match_token(pt.children[0], TokenType.IF)

    index = 1
    if is_next_child_a_token(index, pt, TokenType.NAME):
        index += 1

    index = match_zero_or_more_sexp(index, pt, TokenType.RESULT, _result)

    index = match_zero_or_more_sexp(index, pt, instr_kw, _expr)

    children_left(index, pt, require_at_least_one=True)

    match_sexp(pt.children[index], TokenType.THEN)
    then = pt.children[index]
    index += 1

    index2 = match_zero_or_more_sexp(1, then, instr_kw, _expr)
    children_left(index2, then, require_zero=True)
    then.name = then.children[0].token_type.name

    if is_next_child_a_sexp(index, pt, TokenType.ELSE):
        else_tr = pt.children[index]
        index2 = match_zero_or_more_sexp(1, else_tr, instr_kw, _expr)
        children_left(index2, else_tr, require_zero=True)
        else_tr.name = else_tr.children[0].token_type.name
        index += 1

    children_left(index, pt, require_zero=True)


expr_alts_to_func = {
    TokenType.BLOCK: _block_expr,
    TokenType.LOOP: _loop_expr,
    TokenType.IF: _if_expr
}


def _expr(pt: ListNode):
    match_token(pt.children[0], instr_kw)

    if pt.children[0].token_type in expr_alts:
        expr_alts_to_func[pt.children[0].token_type](pt)
        return

    index = 1
    if pt.children[0].token_type in var_as_arg:
        children_left(index, pt, require_at_least_one=True)
        match_token(pt.children[1], var)
        index += 1
    elif pt.children[0].token_type == TokenType.CONST_INSTR:
        children_left(index, pt, require_at_least_one=True)
        match_token(pt.children[1], {TokenType.NUM, TokenType.NAT})
        index += 1

    index = match_zero_or_more_sexp(index, pt, instr_kw, _expr)

    children_left(index, pt, require_zero=True)
