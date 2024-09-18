from wafunextr.parser.pt_validator.utils import match_token, children_left, is_next_child_a_token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode

val_type = {TokenType.NUM_TYPE}


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

    for poss_val_type in pt.children[index:]:
        match_token(poss_val_type, val_type)


def _param(pt: ListNode):
    _param_local_structure(pt, TokenType.PARAM)


def _local(pt: ListNode):
    _param_local_structure(pt, TokenType.LOCAL)


def _result(pt: ListNode):
    match_token(pt.children[0], TokenType.RESULT)

    for poss_val_type in pt.children[1:]:
        match_token(poss_val_type, val_type)
