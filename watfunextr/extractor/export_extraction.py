from watfunextr.extractor.utils import _process_name_or_idx, _get_mfs_from_dict_keys, _update_idxs
from watfunextr.tokenizer.token_type import TokenType


def _add_export_and_idx_to_update(i, exp_kind_sexp, old2new_exp_idxs, idxs_to_update, mod_idxs_info):
    exp_kind = exp_kind_sexp.children[0].token_type
    old2new_mf_idxs = mod_idxs_info[exp_kind][0]
    mf_info = mod_idxs_info[exp_kind][1]

    mf_idx = _process_name_or_idx(exp_kind_sexp.children[1], mf_info)
    if mf_idx in old2new_mf_idxs:
        if i not in old2new_exp_idxs:
            old2new_exp_idxs[i] = len(old2new_exp_idxs)
        idxs_to_update[exp_kind].append((exp_kind_sexp.children, 1))


def _analyze_exports(mod_idxs_info, exports, module_fields):
    old2new_exp_idxs = {}
    func_idxs_to_update = []
    glob_idxs_to_update = []
    idxs_to_update = {TokenType.FUNC: func_idxs_to_update, TokenType.GLOBAL: glob_idxs_to_update}

    for i, exp in enumerate(exports):
        _add_export_and_idx_to_update(i, exp.children[2], old2new_exp_idxs, idxs_to_update, mod_idxs_info)

    _update_idxs(func_idxs_to_update, mod_idxs_info[TokenType.FUNC][1], mod_idxs_info[TokenType.FUNC][0])
    _update_idxs(glob_idxs_to_update, mod_idxs_info[TokenType.GLOBAL][1], mod_idxs_info[TokenType.GLOBAL][0])

    new_mfs = _get_mfs_from_dict_keys(old2new_exp_idxs, exports)
    module_fields.extend(new_mfs)
