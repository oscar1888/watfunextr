from watfunextr.parser.pt_validator.utils import ops, expr_token_names, var_as_arg
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode, Node

one_arg_tokens = var_as_arg | {TokenType.CONST_INSTR}


def indent(text: str, lvl: int, tab_size: int = 4):
    if not text:
        raise ValueError('Text cannot be empty')
    if lvl < 1:
        raise ValueError('Level of indentation cannot be less than one')
    if tab_size < 1:
        raise ValueError('Tab size cannot be less than one')
    indentation: str = (' '*tab_size)*lvl
    return indentation + text.replace('\n', '\n' + indentation)


def get_or_search_idx(where_to_search_sexp: ListNode, predicate, idx: int = None):
    if idx is not None: return idx

    for i, child in enumerate(where_to_search_sexp.children):
        if predicate(child):
            return i

    return None


def is_an_instr(child: Node) -> bool:
    return (isinstance(child, Token) and child.token_type in ops
            or isinstance(child, ListNode) and child.name in expr_token_names)
