from wafunextr.utils import ListNode
from wafunextr.parser.pt_validator.sections import _module


def _validate(parse_tree: ListNode):
    _module(parse_tree)
    parse_tree.name = parse_tree.children[0].token_type.name
