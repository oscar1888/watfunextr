from watfunextr.parser.pt_validator.utils import match_token, children_left, is_next_child_a_token, \
    match_zero_or_more_token, val_type
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode


def _param_local_structure(pt: ListNode, token_type: TokenType):
    match_token(pt.children[0], token_type)

    index = 1
    if is_next_child_a_token(index, pt, TokenType.NAME):
        index += 1

    if index == 2:
        children_left(index, pt, require_at_least_one=True)
        match_token(pt.children[index], val_type)
        index += 1
        children_left(index, pt, require_zero=True)
        return

    index = match_zero_or_more_token(index, pt, val_type)

    children_left(index, pt, require_zero=True)


def _param(pt: ListNode):
    _param_local_structure(pt, TokenType.PARAM)


def _local(pt: ListNode):
    _param_local_structure(pt, TokenType.LOCAL)


def _result(pt: ListNode):
    match_token(pt.children[0], TokenType.RESULT)

    index = match_zero_or_more_token(1, pt, val_type)

    children_left(index, pt, require_zero=True)
