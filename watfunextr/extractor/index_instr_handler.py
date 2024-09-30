from typing import Tuple
from watfunextr.extractor.utils import _is_sexp_of, _process_name_or_idx
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode
from watfunextr.utils.misc import is_an_instr, get_or_search_idx, one_arg_tokens


def _token_handler(t: Token, sexp: ListNode, idx: int, info: Tuple[list, dict], token_type: TokenType, token_hook, **kwargs) -> int:
    if t.token_type in one_arg_tokens:
        if t.token_type == token_type:
            idx_in_src = _process_name_or_idx(sexp.children[idx + 1], info)
            token_hook(idx_in_src, sexp, idx, **kwargs)
        idx += 1

    return idx


def _if_handler(sexp: ListNode, info: Tuple[list, dict], token_type: TokenType, token_hook, **kwargs):
    then_idx = get_or_search_idx(sexp, _is_sexp_of(TokenType.THEN))
    else_idx = get_or_search_idx(sexp, _is_sexp_of(TokenType.ELSE))

    _main_handler(sexp, info, token_type, token_hook, None, then_idx, **kwargs)
    _main_handler(sexp.children[then_idx], info, token_type, token_hook, **kwargs)
    if else_idx is not None:
        _main_handler(sexp.children[else_idx], info, token_type, token_hook, **kwargs)


def _sexp_handler(sexp: ListNode, info: Tuple[list, dict], token_type: TokenType, token_hook, **kwargs):
    if sexp.name == TokenType.IF.name:
        _if_handler(sexp, info, token_type, token_hook, **kwargs)
        return
    _main_handler(sexp, info, token_type, token_hook, **kwargs)


def _main_handler(sexp: ListNode, info: Tuple[list, dict], token_type: TokenType, token_hook,
                  start_idx: int = None, not_instr_idx: int = None, **kwargs):
    instr_start_idx = get_or_search_idx(sexp, is_an_instr, start_idx)
    if instr_start_idx is None: return

    idx = instr_start_idx
    if not_instr_idx is None: not_instr_idx = len(sexp.children)
    while idx < not_instr_idx:
        child = sexp.children[idx]
        if isinstance(child, Token):
            idx = _token_handler(child, sexp, idx, info, token_type, token_hook, **kwargs)
        else:
            _sexp_handler(child, info, token_type, token_hook, **kwargs)
        idx += 1
