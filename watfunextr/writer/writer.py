from watfunextr.parser.pt_validator.utils import ops, var_as_arg, expr_token_names
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.utils import ListNode
from watfunextr.utils.misc import indent


def _write_sexp(sexp: ListNode) -> str:
    if sexp.children[0].token_type in {TokenType.FUNC, TokenType.BLOCK, TokenType.LOOP, TokenType.IF, TokenType.THEN, TokenType.ELSE}:
        str_sexp: str = '('
        to_add = []
        next_instr_idx = -1
        for i, child in enumerate(sexp.children):
            if isinstance(child, ListNode) and child.name in expr_token_names or isinstance(child, Token) and child.token_type in ops:
                next_instr_idx = i
                break
            to_add.append(child.token_value if isinstance(child, Token) else _write_sexp(child))
        str_sexp += ' '.join(to_add)

        if next_instr_idx == -1:
            return str_sexp + ')'

        idx = next_instr_idx
        while idx < len(sexp.children):
            child = sexp.children[idx]
            if isinstance(child, Token) and (child.token_type in var_as_arg or child.token_type == TokenType.CONST_INSTR):
                str_sexp += '\n' + indent(f'{child.token_value} {sexp.children[idx+1].token_value}', 1)
                idx += 1
            elif isinstance(child, ListNode):
                str_sexp += '\n' + indent(_write_sexp(child), 1)
            else:
                str_sexp += '\n' + indent(child.token_value, 1)
            idx += 1

        return str_sexp + '\n)'

    return '(' + ' '.join(sexp.children[i].token_value if isinstance(sexp.children[i], Token) else _write_sexp(sexp.children[i]) for i in range(len(sexp.children))) + ')'


def write_from_module_fields(module_fields: list[ListNode]) -> str:
    module_fields_text: str = '\n'.join(indent(_write_sexp(mf), 1) for mf in module_fields)
    return f'(module\n{module_fields_text}\n)'
