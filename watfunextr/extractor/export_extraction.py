from watfunextr.extractor.utils import _process_name_or_idx, _get_mfs_from_dict_keys, _update_idxs
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType


def _export_handler(i, exp_inner_sexp, old2new_idxs, idxs_to_update, old2new_fun_idxs, fun_info, old2new_glob_idxs, glob_info):
    exp_kind = exp_inner_sexp.children[0].token_type
    if exp_kind == TokenType.FUNC:
        fun_idx = _process_name_or_idx(exp_inner_sexp.children[1], fun_info)
        if fun_idx in old2new_fun_idxs:
            if i not in old2new_idxs:
                old2new_idxs[i] = len(old2new_idxs)
            idxs_to_update.append((TokenType.FUNC, exp_inner_sexp.children, 1))
    elif exp_kind == TokenType.GLOBAL:
        glob_idx = _process_name_or_idx(exp_inner_sexp.children[1], glob_info)
        if glob_idx in old2new_glob_idxs:
            if i not in old2new_idxs:
                old2new_idxs[i] = len(old2new_idxs)
            idxs_to_update.append((TokenType.GLOBAL, exp_inner_sexp.children, 1))


def _analyze_exports(old2new_fun_idxs, fun_info, old2new_glob_idxs, glob_info, exports, module_fields):
    old2new_idxs = {}
    idxs_to_update = []

    for i, exp in enumerate(exports):
        _export_handler(i, exp.children[2], old2new_idxs, idxs_to_update, old2new_fun_idxs, fun_info, old2new_glob_idxs, glob_info)

    func_idxs_to_update = list(filter(lambda e: e[0] == TokenType.FUNC, idxs_to_update))
    glob_idxs_to_update = list(filter(lambda e: e[0] == TokenType.GLOBAL, idxs_to_update))

    _update_idxs(list(map(lambda e: (e[1], e[2]), func_idxs_to_update)), fun_info, old2new_fun_idxs)
    _update_idxs(list(map(lambda e: (e[1], e[2]), glob_idxs_to_update)), glob_info, old2new_glob_idxs)

    new_mfs = _get_mfs_from_dict_keys(old2new_idxs, exports)
    module_fields.extend(new_mfs)

    return old2new_idxs, idxs_to_update
