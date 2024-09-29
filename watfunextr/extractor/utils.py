from typing import Tuple, Union
from watfunextr.extractor import ExtractionError
from watfunextr.parser.pt_validator.utils import ops, expr_token_names
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import Node, ListNode


def _is_sexp_of(token_type: TokenType):
    return lambda sexp: isinstance(sexp, ListNode) and sexp.name == token_type.name


def _is_an_instr(child: Node) -> bool:
    return (isinstance(child, Token) and child.token_type in ops
            or isinstance(child, ListNode) and child.name in expr_token_names)


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


def _get_or_search_idx(where_to_search_sexp: ListNode, predicate, idx: int = None):
    if idx is not None: return idx

    for i, child in enumerate(where_to_search_sexp.children):
        if predicate(child):
            return i


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
