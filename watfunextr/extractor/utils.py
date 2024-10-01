from typing import Tuple, Union
from watfunextr.extractor import ExtractionError
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _get_mfs_from_dict_keys(d: dict, new_mfs_list: list) -> list:
    return list(map(lambda e: new_mfs_list[e], d.keys()))


def _is_sexp_of(token_type: TokenType):
    def specific_is_sexp_of(sexp):
        return isinstance(sexp, ListNode) and sexp.name == token_type.name
    return specific_is_sexp_of


def _has_name(sexp: ListNode) -> bool:
    return (len(sexp.children) >= 2
            and isinstance(sexp.children[1], Token)
            and sexp.children[1].token_type == TokenType.NAME)


def _get_name2idx(l: list[ListNode]) -> dict:
    d = {}
    for i, el in enumerate(l):
        if _has_name(el):
            if el.children[1].token_value in d:
                raise ExtractionError('Duplicated name', (el.children[1].line, el.children[1].col))
            d[el.children[1].token_value] = i

    return d


def _get_module_fields(pt: ListNode, token_type: TokenType) -> list[ListNode]:
    return [c for c in pt.children if _is_sexp_of(token_type)(c)]


def _update_idxs(idxs_to_update: list, info, old2new_idxs: dict):
    for children, idx in idxs_to_update:
        mf_idx = _process_name_or_idx(children[idx], info)
        children[idx] = Token(TokenType.NAT, str(old2new_idxs[mf_idx]), 1, 1)


def _search_in_funs(new_funs: list[ListNode], info: Tuple[list, dict], fun_handler) -> Tuple[dict, list]:
    old2new_idxs = {}
    idxs_to_update = []

    for fun in new_funs:
        fun_handler(fun, old2new_idxs, idxs_to_update, info)

    return old2new_idxs, idxs_to_update


def _process_name_or_idx(name_or_idx: Token, info: Tuple[list, dict]) -> int:
    arg = name_or_idx.token_value
    if arg.isdigit(): arg = int(arg)
    return _get_idx(arg, info, (name_or_idx.line, name_or_idx.col))


def _get_idx(idx_or_name: Union[int, str], info, line_col: Tuple[int, int] = None) -> int:
    if isinstance(idx_or_name, int):
        if idx_or_name < 0:
            raise ExtractionError('Indexes start from 0', line_col)
        if idx_or_name >= len(info[0]):
            raise ExtractionError(f'Index {idx_or_name} does not exist', line_col)
    else:
        if not idx_or_name or idx_or_name[0] != '$':
            raise ExtractionError('Names must start with $ symbol', line_col)
        if idx_or_name not in info[1]:
            raise ExtractionError(f'{idx_or_name} is not a name in the WAT module', line_col)

    return info[1][idx_or_name] if isinstance(idx_or_name, str) else idx_or_name
