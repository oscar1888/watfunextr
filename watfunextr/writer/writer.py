from watfunextr.parser.pt_validator.utils import instr_kw, ops, var_as_arg
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode
from watfunextr.utils.misc import indent

_expr_token_names = {t.name for t in instr_kw}
_op_token_names = {t.name for t in ops}


def _write_sexp(sexp: ListNode) -> str:
    if sexp.children[0].token_type == TokenType.FUNC:
        str_sexp: str = '('
        to_add = []
        next_instr_idx = -1
        for i, child in enumerate(sexp.children):
            if isinstance(child, ListNode) and child.name in _expr_token_names or isinstance(child, Token) and child in _op_token_names:
                next_instr_idx = i
                break
            to_add.append(child.token_value if isinstance(child, Token) else _write_sexp(child))
        str_sexp += ' '.join(to_add)

        if next_instr_idx == -1:
            return str_sexp + ')'

        idx = next_instr_idx
        while idx < len(sexp.children):
            child = sexp.children[idx]
            if isinstance(child, Token) and child.token_type in var_as_arg:
                str_sexp += '\n' + indent(f'{child.token_value} {sexp.children[idx+1].token_value}', 1)
            else:
                str_sexp += '\n' + indent(_write_sexp(child), 1)
            idx += 1

        return str_sexp + '\n)'

    return '(' + ' '.join(sexp.children[i].token_value if isinstance(sexp.children[i], Token) else _write_sexp(sexp.children[i]) for i in range(len(sexp.children))) + ')'


def write_from_module_fields(module_fields: list[ListNode]) -> str:
    module_fields_text: str = '\n'.join(indent(_write_sexp(mf), 1) for mf in module_fields)
    return f'(module\n{module_fields_text}\n)'
