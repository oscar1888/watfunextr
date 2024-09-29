from typing import Union
from watfunextr.extractor.utils import _get_idx, _get_or_search_idx, _is_sexp_of, _is_an_instr, _get_name2idx, \
    _get_module_fields
from watfunextr.parser.pt_validator.utils import var_as_arg
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _token_handler(t: Token, sexp: ListNode, idx: int, functions: list[ListNode], name2idx: dict, adjacents: list) -> int:
    if t.token_type in var_as_arg or t.token_type == TokenType.CONST_INSTR:
        if t.token_type == TokenType.CALL:
            fun_name_or_idx = sexp.children[idx + 1]
            arg = fun_name_or_idx.token_value
            if arg.isdigit(): arg = int(arg)
            fun_idx = _get_idx(arg, functions, name2idx, (fun_name_or_idx.line, fun_name_or_idx.col))
            adjacents.append((fun_idx, (sexp.children, idx+1)))
        idx += 1

    return idx


def _if_handler(sexp: ListNode, adjacents: list, functions: list[ListNode], name2idx: dict):
    then_idx = _get_or_search_idx(sexp, _is_sexp_of(TokenType.THEN))
    else_idx = _get_or_search_idx(sexp, _is_sexp_of(TokenType.ELSE))
    adjacents.extend(_get_adjacents(sexp, functions, name2idx, None, then_idx))
    adjacents.extend(_get_adjacents(sexp.children[then_idx], functions, name2idx))
    if else_idx is not None:
        adjacents.extend(_get_adjacents(sexp.children[else_idx], functions, name2idx))


def _op_expr_handler(sexp: ListNode, functions: list[ListNode], name2idx: dict, adjacents: list):
    idx2 = _token_handler(sexp.children[0], sexp, 0, functions, name2idx, adjacents)
    idx2 += 1
    adjacents.extend(_get_adjacents(sexp, functions, name2idx, idx2))


def _sexp_handler(sexp: ListNode, adjacents: list, functions: list[ListNode], name2idx: dict):
    if sexp.name in {TokenType.BLOCK.name, TokenType.LOOP.name}:
        adjacents.extend(_get_adjacents(sexp, functions, name2idx))
    elif sexp.name == TokenType.IF.name:
        _if_handler(sexp, adjacents, functions, name2idx)
    else:
        _op_expr_handler(sexp, functions, name2idx, adjacents)


def _get_adjacents(sexp: ListNode, functions: list[ListNode], name2idx: dict, start_idx: int = None, not_instr_idx: int = None):
    instr_start_idx = _get_or_search_idx(sexp, _is_an_instr, start_idx)
    if instr_start_idx is None: return []

    adjacents = []
    idx = instr_start_idx
    if not_instr_idx is None: not_instr_idx = len(sexp.children)
    while idx < not_instr_idx:
        child = sexp.children[idx]
        if isinstance(child, Token):
            idx = _token_handler(child, sexp, idx, functions, name2idx, adjacents)
        else:
            _sexp_handler(child, adjacents, functions, name2idx)
        idx += 1

    return adjacents


def _navigate_fun_call_graph(functions: list[ListNode], name2idx: dict, fun_idx: int):
    # DFS search in function call graph
    fun_idx_to_update = []

    stack = [fun_idx]
    old_to_new_idxs = {}  # note that the keys list is the set of visited functions
    while len(stack) != 0:
        curr = stack.pop()
        if curr not in old_to_new_idxs:
            old_to_new_idxs[curr] = len(old_to_new_idxs)
            for adj, fun_idx_info in _get_adjacents(functions[curr], functions, name2idx)[::-1]:
                fun_idx_to_update.append(fun_idx_info)
                if adj not in old_to_new_idxs:
                    stack.append(adj)

    return old_to_new_idxs, fun_idx_to_update


def _update_idxs(idxs_to_update, old_list, name2idx, old2new_idxs):
    for children, idx in idxs_to_update:
        arg = children[idx].token_value
        if arg.isdigit(): arg = int(arg)
        mf_idx = _get_idx(arg, old_list, name2idx, (children[idx].line, children[idx].col))
        children[idx] = Token(TokenType.NAT, str(old2new_idxs[mf_idx]), 1, 1)


def _typedef_handler(fun, old2new_idxs, idxs_to_update, info):
    if len(fun.children) >= 2 and _is_sexp_of(TokenType.TYPE)(fun.children[1]):
        fun_child_idx = 1
    elif len(fun.children) >= 3 and _is_sexp_of(TokenType.TYPE)(fun.children[2]):
        fun_child_idx = 2
    else:
        return

    sexp = fun.children[fun_child_idx]
    name_or_idx = sexp.children[1]
    arg = name_or_idx.token_value
    if arg.isdigit(): arg = int(arg)
    idx = _get_idx(arg, info[0], info[1], (name_or_idx.line, name_or_idx.col))

    if idx not in old2new_idxs:
        old2new_idxs[idx] = len(old2new_idxs)
    idxs_to_update.append((sexp.children, 1))


def _search_in_funs(new_funs, info, fun_handler):
    old2new_idxs = {}
    idxs_to_update = []

    for fun in new_funs:
        fun_handler(fun, old2new_idxs, idxs_to_update, info)

    return old2new_idxs, idxs_to_update


def _get_fun_with_dependencies(function_info, typedef_info, fun_idx: int):
    module_fields = []

    old2new_fun_idxs, fun_idx_to_update = _navigate_fun_call_graph(function_info[0], function_info[1], fun_idx)
    _update_idxs(fun_idx_to_update, function_info[0], function_info[1], old2new_fun_idxs)
    new_funs = list(map(lambda e: function_info[0][e], old2new_fun_idxs.keys()))
    module_fields.extend(new_funs)

    old2new_typedef_idxs, type_idx_to_update = _search_in_funs(new_funs, typedef_info, _typedef_handler)
    _update_idxs(type_idx_to_update, typedef_info[0], typedef_info[1], old2new_typedef_idxs)
    new_typedefs = list(map(lambda e: typedef_info[0][e], old2new_typedef_idxs.keys()))
    module_fields.extend(new_typedefs)

    return module_fields


def extract(pt: ListNode, fun_idx_or_name: Union[int, str]):
    functions = _get_module_fields(pt, TokenType.FUNC)
    name2idx_funs = _get_name2idx(functions)
    fun_idx = _get_idx(fun_idx_or_name, functions, name2idx_funs)

    typedefs = _get_module_fields(pt, TokenType.TYPE)
    name2idx_typedefs = _get_name2idx(typedefs)

    module_fields = _get_fun_with_dependencies((functions, name2idx_funs), (typedefs, name2idx_typedefs), fun_idx)

    return module_fields
