from typing import Tuple
from watfunextr.extractor.index_instr_handler import _main_handler
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _global_handler(fun: ListNode, old2new_idxs: dict, idxs_to_update: list, info: Tuple[list, dict],
                    start_idx: int = None, not_instr_idx: int = None):
    def _hook(idx_in_src, inner_sexp, idx, **kwargs):
        if idx_in_src not in kwargs['old2new_idxs']:
            kwargs['old2new_idxs'][idx_in_src] = len(kwargs['old2new_idxs'])
        kwargs['idxs_to_update'].append((inner_sexp.children, idx + 1))

    _main_handler(fun, info, TokenType.GLOBAL_INSTR, _hook, start_idx, not_instr_idx,
                  old2new_idxs=old2new_idxs, idxs_to_update=idxs_to_update)
