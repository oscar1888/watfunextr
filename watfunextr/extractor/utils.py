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


def _func_has_name(func: ListNode):
    return (len(func.children) >= 2
            and isinstance(func.children[1], Token)
            and func.children[1].token_type == TokenType.NAME)


def _get_fun_names(funcs: list[ListNode]) -> dict:
    d = {}
    for i, func in enumerate(funcs):
        if _func_has_name(func):
            if func.children[1].token_value in d:
                raise ExtractionError('Duplicated function name', (func.children[1].line, func.children[1].col))
            d[func.children[1].token_value] = i

    return d


def _get_funs(pt: ListNode) -> Tuple[list, dict]:
    funcs = [child for child in pt.children if _is_sexp_of(TokenType.FUNC)(child)]
    return funcs, _get_fun_names(funcs)


def _get_or_search_idx(where_to_search_sexp: ListNode, predicate, idx: int = None):
    if idx is not None: return idx

    for i, child in enumerate(where_to_search_sexp.children):
        if predicate(child):
            return i


def _get_fun_idx(fun_idx_or_name: Union[int, str], functions: list[ListNode], name2idx: dict,
                 line_col: Tuple[int, int] = None) -> int:
    if isinstance(fun_idx_or_name, int):
        if fun_idx_or_name < 0:
            raise ExtractionError('Function indexes start from 0', line_col)
        if fun_idx_or_name >= len(functions):
            raise ExtractionError(f'Function at index {fun_idx_or_name} does not exist', line_col)
    else:
        if not fun_idx_or_name or fun_idx_or_name[0] != '$':
            raise ExtractionError('Function names must start with $ symbol', line_col)
        if fun_idx_or_name not in name2idx:
            raise ExtractionError(f'There is no function called {fun_idx_or_name} in the WAT module', line_col)

    return name2idx[fun_idx_or_name] if isinstance(fun_idx_or_name, str) else fun_idx_or_name
