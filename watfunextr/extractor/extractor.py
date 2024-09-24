from typing import Tuple, Union

from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode, Node


def _is_func(child: Node) -> bool:
    return isinstance(child, ListNode) and child.name == TokenType.FUNC.name


def _get_fun_names(funcs: list[ListNode]):
    return {
        func.children[1].token_value: i
        for i, func in enumerate(funcs)
        if len(func.children) >= 2
           and isinstance(func.children[1], Token)
           and func.children[1].token_type == TokenType.NAME
    }


def _get_funs(pt: ListNode) -> Tuple[list, dict]:
    funcs = [child for child in pt.children if _is_func(child)]
    return funcs, _get_fun_names(funcs)


def extract(pt: ListNode, fun_idx_or_name: Union[int, str]) -> list[ListNode]:
    functions, name2idx = _get_funs(pt)
    if isinstance(fun_idx_or_name, str):
        if not fun_idx_or_name or fun_idx_or_name[0] != '$':
            raise ValueError('Function names must start with $ symbol')
        if fun_idx_or_name not in name2idx:
            raise ValueError(f'There is no function called {fun_idx_or_name} in the WAT module')
    fun_idx = name2idx[fun_idx_or_name] if isinstance(fun_idx_or_name, str) else fun_idx_or_name
    if fun_idx < 0:
        raise ValueError('Function indexes start from 0')
    if fun_idx >= len(functions):
        raise ValueError(f'Function at index {fun_idx} does not exist')

    return [functions[fun_idx]]
