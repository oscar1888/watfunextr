from typing import Union
from watfunextr.extractor.func_extraction import _navigate_fun_call_graph
from watfunextr.extractor.typedef_extraction import _typedef_handler
from watfunextr.extractor.utils import _get_idx, _get_name2idx, _get_module_fields, _update_idxs, _search_in_funs
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


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
