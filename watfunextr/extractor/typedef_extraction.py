from typing import Tuple
from watfunextr.extractor.utils import _is_sexp_of, _process_name_or_idx
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode
from watfunextr.utils.misc import get_or_search_idx


def _typedef_handler(fun: ListNode, old2new_idxs: dict, idxs_to_update: list, info: Tuple[list, dict]):
    fun_child_idx = get_or_search_idx(fun, _is_sexp_of(TokenType.TYPE))
    if fun_child_idx is None: return

    sexp = fun.children[fun_child_idx]
    idx = _process_name_or_idx(sexp.children[1], info)

    if idx not in old2new_idxs:
        old2new_idxs[idx] = len(old2new_idxs)
    idxs_to_update.append((sexp.children, 1))
