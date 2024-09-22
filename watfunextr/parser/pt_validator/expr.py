from watfunextr.parser.pt_validator.param_local_result import _result
from watfunextr.parser.pt_validator.utils import instr_kw, expr_alts, match_token, children_left, match_sexp, \
    next_child_and_is_a_token, match_zero_or_more_sexp, next_child_and_is_a_sexp, match_zero_or_more_tokens_or_sexp_rule, ops, _op
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _block_loop_structure(pt: ListNode, token_type: TokenType):
    match_token(pt.children[0], token_type)

    index = 1
    if next_child_and_is_a_token(index, pt, TokenType.NAME):
        index += 1

    if next_child_and_is_a_sexp(index, pt, TokenType.RESULT):
        _result(pt.children[index])
        pt.children[index].name = pt.children[index].children[0].token_type.name
        index += 1

    index = match_zero_or_more_tokens_or_sexp_rule(index, pt, ops, instr_kw, _op, _expr)

    children_left(index, pt, require_zero=True)


def _block_expr(pt: ListNode):
    _block_loop_structure(pt, TokenType.BLOCK)


def _loop_expr(pt: ListNode):
    _block_loop_structure(pt, TokenType.LOOP)


def _if_expr(pt: ListNode):
    match_token(pt.children[0], TokenType.IF)

    index = 1
    if next_child_and_is_a_token(index, pt, TokenType.NAME):
        index += 1

    if next_child_and_is_a_sexp(index, pt, TokenType.RESULT):
        _result(pt.children[index])
        pt.children[index].name = pt.children[index].children[0].token_type.name
        index += 1

    index = match_zero_or_more_sexp(index, pt, instr_kw, _expr)

    children_left(index, pt, require_at_least_one=True)

    match_sexp(pt.children[index], TokenType.THEN)
    then = pt.children[index]
    index += 1

    index2 = match_zero_or_more_tokens_or_sexp_rule(1, then, ops, instr_kw, _op, _expr)
    children_left(index2, then, require_zero=True)
    then.name = then.children[0].token_type.name

    if next_child_and_is_a_sexp(index, pt, TokenType.ELSE):
        else_tr = pt.children[index]
        index2 = match_zero_or_more_tokens_or_sexp_rule(1, else_tr, ops, instr_kw, _op, _expr)
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

    index = _op(0, pt)

    index = match_zero_or_more_sexp(index, pt, instr_kw, _expr)

    children_left(index, pt, require_zero=True)
