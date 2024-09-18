from wafunextr.parser.pt_validator.expr import _expr
from wafunextr.parser.pt_validator.param_local_result import _param, _result, _local
from wafunextr.parser.pt_validator.utils import var, instr_kw, match_token, children_left, match_sexp, \
    is_next_child_a_token, match_zero_or_more_sexp, is_next_child_a_sexp
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode


def _func(pt: ListNode):
    match_token(pt.children[0], TokenType.FUNC)

    index = 1
    if is_next_child_a_token(index, pt, TokenType.NAME):
        index += 1

    if is_next_child_a_sexp(index, pt, TokenType.TYPE):
        func_type = pt.children[index]
        index2 = 1
        children_left(index2, func_type, require_at_least_one=True)
        match_token(func_type.children[1], var)
        index2 += 1
        children_left(index2, func_type, require_zero=True)
        func_type.name = func_type.children[0].token_type.name
        index += 1

    index = match_zero_or_more_sexp(index, pt, TokenType.PARAM, _param)

    index = match_zero_or_more_sexp(index, pt, TokenType.RESULT, _result)

    index = match_zero_or_more_sexp(index, pt, TokenType.LOCAL, _local)

    index = match_zero_or_more_sexp(index, pt, instr_kw, _expr)

    children_left(index, pt, require_zero=True)


def _typedef(pt: ListNode):
    match_token(pt.children[0], TokenType.TYPE)

    index = 1
    if is_next_child_a_token(index, pt, TokenType.NAME):
        index += 1

    children_left(index, pt, require_at_least_one=True)

    match_sexp(pt.children[index], TokenType.FUNC)
    func_typedef = pt.children[index]
    index += 1

    index2 = match_zero_or_more_sexp(1, func_typedef, TokenType.PARAM, _param)

    index2 = match_zero_or_more_sexp(index2, func_typedef, TokenType.RESULT, _result)

    children_left(index2, func_typedef, require_zero=True)
    func_typedef.name = func_typedef.children[0].token_type.name

    children_left(index, pt, require_zero=True)


module_fields = {TokenType.TYPE: _typedef, TokenType.FUNC: _func}


def _module(pt: ListNode):
    match_token(pt.children[0], TokenType.MODULE)

    index = 1
    if is_next_child_a_token(index, pt, TokenType.NAME):
        index += 1

    for poss_module_field in pt.children[index:]:
        match_sexp(poss_module_field, module_fields)
        _section = module_fields[poss_module_field.children[0].token_type]
        _section(poss_module_field)
        poss_module_field.name = poss_module_field.children[0].token_type.name
