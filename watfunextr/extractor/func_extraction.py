from typing import Tuple
from watfunextr.extractor.index_instr_handler import _main_handler
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _get_adjacents(sexp: ListNode, info, start_idx: int = None, not_instr_idx: int = None) -> list:
    adjacents = []

    def _hook(idx_read_in_src: int, inner_sexp: ListNode, idx: int, **kwargs):
        kwargs['adjacents'].append((idx_read_in_src, (inner_sexp.children, idx + 1)))

    _main_handler(sexp, info, TokenType.CALL, _hook, start_idx, not_instr_idx, adjacents=adjacents)

    return adjacents


def _navigate_fun_call_graph(info: Tuple[list, dict], fun_idx: int) -> Tuple[dict, list]:
    # DFS search in function call graph
    fun_idx_to_update = []

    stack = [fun_idx]
    old_to_new_idxs = {}  # note that the keys list is the set of visited functions
    while len(stack) != 0:
        curr = stack.pop()
        if curr not in old_to_new_idxs:
            old_to_new_idxs[curr] = len(old_to_new_idxs)
            for adj, fun_idx_info in _get_adjacents(info[0][curr], info)[::-1]:
                fun_idx_to_update.append(fun_idx_info)
                if adj not in old_to_new_idxs:
                    stack.append(adj)

    return old_to_new_idxs, fun_idx_to_update
