from watfunextr.parser.pt_validator.utils import var_as_arg
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode
from watfunextr.utils.misc import indent, get_or_search_idx, is_an_instr

_to_indent_sexps = {TokenType.FUNC, TokenType.BLOCK, TokenType.LOOP, TokenType.IF, TokenType.THEN, TokenType.ELSE}

_one_arg_tokens = var_as_arg | {TokenType.CONST_INSTR}


def _write_node(c):
    return c.token_value if isinstance(c, Token) else _write_sexp(c)


def _write_sexp(sexp: ListNode) -> str:
    if sexp.children[0].token_type in _to_indent_sexps:
        str_sexp: str = '('

        next_instr_idx = get_or_search_idx(sexp, is_an_instr)
        str_sexp += ' '.join(_write_node(c) for c in sexp.children[:next_instr_idx])
        if next_instr_idx is None: return str_sexp + ')'

        idx = next_instr_idx
        while idx < len(sexp.children):
            child = sexp.children[idx]
            if isinstance(child, Token) and child.token_type in _one_arg_tokens:
                str_sexp += '\n' + indent(f'{child.token_value} {sexp.children[idx+1].token_value}', 1)
                idx += 1
            elif isinstance(child, ListNode):
                str_sexp += '\n' + indent(_write_sexp(child), 1)
            else:
                str_sexp += '\n' + indent(child.token_value, 1)
            idx += 1

        return str_sexp + '\n)'

    return '(' + ' '.join(_write_node(c) for c in sexp.children) + ')'


def write_from_module_fields(module_fields: list[ListNode]) -> str:
    module_fields_text: str = '\n'.join(indent(_write_sexp(mf), 1) for mf in module_fields)
    return f'(module\n{module_fields_text}\n)'
