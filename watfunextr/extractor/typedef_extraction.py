from watfunextr.extractor.utils import _is_sexp_of, _get_or_search_idx, _process_name_or_idx
from watfunextr.tokenizer.token_type import TokenType


def _typedef_handler(fun, old2new_idxs, idxs_to_update, info):
    fun_child_idx = _get_or_search_idx(fun, _is_sexp_of(TokenType.TYPE))
    if fun_child_idx is None: return

    sexp = fun.children[fun_child_idx]
    idx = _process_name_or_idx(sexp.children[1], info)

    if idx not in old2new_idxs:
        old2new_idxs[idx] = len(old2new_idxs)
    idxs_to_update.append((sexp.children, 1))
