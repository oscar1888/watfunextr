from typing import Tuple, Union
from watfunextr.extractor import ExtractionError
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _is_sexp_of(token_type: TokenType):
    def specific_is_sexp_of(sexp):
        return isinstance(sexp, ListNode) and sexp.name == token_type.name
    return specific_is_sexp_of


def _has_name(sexp: ListNode):
    return (len(sexp.children) >= 2
            and isinstance(sexp.children[1], Token)
            and sexp.children[1].token_type == TokenType.NAME)


def _get_name2idx(l: list[ListNode]):
    d = {}
    for i, el in enumerate(l):
        if _has_name(el):
            if el.children[1].token_value in d:
                raise ExtractionError('Duplicated name', (el.children[1].line, el.children[1].col))
            d[el.children[1].token_value] = i

    return d


def _get_module_fields(pt: ListNode, token_type: TokenType):
    return [c for c in pt.children if _is_sexp_of(token_type)(c)]


def _update_idxs(idxs_to_update, old_list, name2idx, old2new_idxs):
    for children, idx in idxs_to_update:
        arg = children[idx].token_value
        if arg.isdigit(): arg = int(arg)
        mf_idx = _get_idx(arg, old_list, name2idx, (children[idx].line, children[idx].col))
        children[idx] = Token(TokenType.NAT, str(old2new_idxs[mf_idx]), 1, 1)


def _search_in_funs(new_funs, info, fun_handler):
    old2new_idxs = {}
    idxs_to_update = []

    for fun in new_funs:
        fun_handler(fun, old2new_idxs, idxs_to_update, info)

    return old2new_idxs, idxs_to_update


def _process_name_or_idx(name_or_idx, info):
    arg = name_or_idx.token_value
    if arg.isdigit(): arg = int(arg)
    return _get_idx(arg, info[0], info[1], (name_or_idx.line, name_or_idx.col))


def _get_idx(idx_or_name: Union[int, str], old_list: list[ListNode], name2idx: dict, line_col: Tuple[int, int] = None) -> int:
    if isinstance(idx_or_name, int):
        if idx_or_name < 0:
            raise ExtractionError('Indexes start from 0', line_col)
        if idx_or_name >= len(old_list):
            raise ExtractionError(f'Index {idx_or_name} does not exist', line_col)
    else:
        if not idx_or_name or idx_or_name[0] != '$':
            raise ExtractionError('Names must start with $ symbol', line_col)
        if idx_or_name not in name2idx:
            raise ExtractionError(f'{idx_or_name} is not a name in the WAT module', line_col)

    return name2idx[idx_or_name] if isinstance(idx_or_name, str) else idx_or_name
