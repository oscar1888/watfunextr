from typing import Union, Tuple
from watfunextr.extractor.export_extraction import _analyze_exports
from watfunextr.extractor.func_extraction import _navigate_fun_call_graph
from watfunextr.extractor.global_extraction import _global_handler
from watfunextr.extractor.typedef_extraction import _typedef_handler
from watfunextr.extractor.utils import _get_idx, _get_name2idx, _get_module_fields, _update_idxs, _search_in_funs, \
    _get_mfs_from_dict_keys
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _update_src_and_add_mfs(funs_or_search_res: Union[list, Tuple], info: Tuple[list, dict], module_fields: list, handler=None):
    old2new_idxs, idxs_to_update = (
        _search_in_funs(funs_or_search_res, info, handler)
        if isinstance(funs_or_search_res, list)
        else funs_or_search_res
    )
    _update_idxs(idxs_to_update, info, old2new_idxs)
    new_mfs = _get_mfs_from_dict_keys(old2new_idxs, info[0])
    module_fields.extend(new_mfs)
    return new_mfs, old2new_idxs


def _get_fun_with_dependencies(info_mapping: dict, fun_idx: int):
    module_fields = []

    search_fun_res = _navigate_fun_call_graph(info_mapping[TokenType.FUNC.name], fun_idx)
    new_funs, _ = _update_src_and_add_mfs(search_fun_res, info_mapping[TokenType.FUNC.name], module_fields)

    _update_src_and_add_mfs(new_funs, info_mapping[TokenType.TYPE.name], module_fields, _typedef_handler)
    _, old2new_glob_idxs = _update_src_and_add_mfs(new_funs, info_mapping[TokenType.GLOBAL.name], module_fields, _global_handler)
    _analyze_exports(
        search_fun_res[0], info_mapping[TokenType.FUNC.name],
        old2new_glob_idxs, info_mapping[TokenType.GLOBAL.name],
        info_mapping[TokenType.EXPORT.name][0],
        module_fields
    )

    return module_fields


def _fill_info(pt, info_mapping, token_type: TokenType, no_name=False):
    mfs = _get_module_fields(pt, token_type)
    name2idx = _get_name2idx(mfs) if not no_name else {}
    info_mapping[token_type.name] = (mfs, name2idx)


def extract(pt: ListNode, fun_idx_or_name: Union[int, str]):
    info_mapping = {}

    _fill_info(pt, info_mapping, TokenType.FUNC)
    _fill_info(pt, info_mapping, TokenType.TYPE)
    _fill_info(pt, info_mapping, TokenType.GLOBAL)
    _fill_info(pt, info_mapping, TokenType.EXPORT, no_name=True)

    fun_idx = _get_idx(fun_idx_or_name, info_mapping[TokenType.FUNC.name])
    module_fields = _get_fun_with_dependencies(info_mapping, fun_idx)

    return module_fields
