import unittest

from tests.utils import read
from wafunextr.parser import parse
from wafunextr.parser.parser_error import ParserError
from wafunextr.tokenizer import tokenize
from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.utils import ListNode


class SExprParser(unittest.TestCase):
    def test_simple_module(self):
        self.assertEqual(
            parse(tokenize(read('misc/simple_module.wat'))),
            ListNode(1,1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2))
        )

    def test_add_module(self):
        self.assertEqual(
            parse(tokenize(read('misc/add.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(3, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 3, 6),
                    Token(TokenType.NAME, '$add', 3, 11),
                    ListNode(3, 16, 'PARAM',
                        Token(TokenType.PARAM, 'param', 3, 17),
                        Token(TokenType.NAME, '$a', 3, 23),
                        Token(TokenType.NUM_TYPE, 'i32', 3, 26)
                        ),
                    ListNode(3, 31, 'PARAM',
                        Token(TokenType.PARAM, 'param', 3, 32),
                        Token(TokenType.NAME, '$b', 3, 38),
                        Token(TokenType.NUM_TYPE, 'i32', 3, 41)
                        ),
                    ListNode(3, 46, 'RESULT',
                        Token(TokenType.RESULT, 'result', 3, 47),
                        Token(TokenType.NUM_TYPE, 'i32', 3, 54)
                        ),
                    ListNode(4, 9, 'INT_INSTR',
                        Token(TokenType.INT_INSTR, 'i32.add', 4, 10),
                        ListNode(4, 18, 'LOCAL_INSTR',
                            Token(TokenType.LOCAL_INSTR, 'local.get', 4, 19),
                            Token(TokenType.NAME, '$a', 4, 29)
                        ),
                        ListNode(4, 33, 'LOCAL_INSTR',
                                 Token(TokenType.LOCAL_INSTR, 'local.get', 4, 34),
                                 Token(TokenType.NAME, '$b', 4, 44)
                        )
                    )
                )
            )
        )

    def test_empty_program(self):
        with self.assertRaises(ValueError) as ctx:
            parse([])

        self.assertEqual(str(ctx.exception), 'The program must include at least one token')

    def test_exceeding_right_par(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/exceeding_right_par.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 3:2: unexpected ')'")

    def test_unclosed_par(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/unclosed_par.wat')))

        self.assertEqual(str(ctx.exception), 'Syntax error: there are 2 unclosed parenthesis')

    def test_empty_par(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/empty_par.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:6: unexpected ')'")

    def test_not_sexp_module(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/not_sexp_module.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:1: unexpected 'module'")

    # MODULE RULE

    def test_wrong_module_grammar(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/module/wrong_module_grammar.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:2: unexpected '$add'")

    def test_name_after_module_field(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/module/name_after_module_field.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:23: unexpected '$a'")

    def test_unexpected_after_module_fields(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/module/unexpected_after_module_fields.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:26: unexpected '('")

    # TYPEDEF RULE

    def test_required_inner_sexp_not_present(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/typedef/required_inner_sexp_not_present.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:17: unexpected ')'")

    def test_swapped_rules_in_inner_sexp(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/typedef/swapped_rules_in_inner_sexp.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:33: unexpected '('")

    def test_unexpected(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/typedef/unexpected.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:22: unexpected 'block'")

    def test_unexpected_in_inner_func_sexp(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/typedef/unexpected_in_inner_func_sexp.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 1:33: unexpected '('")

    # PARAM LOCAL

    def test_multiple_val_type_after_name(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/param_local/multiple_val_type_after_name.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:31: unexpected 'i32'")

    def test_unexpected_in_local_without_name(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/param_local/unexpected_in_local_without_name.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:26: unexpected '('")

    def test_name_not_present(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/param_local/name_not_present.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'TYPE',
                    Token(TokenType.TYPE, 'type', 2, 6),
                    ListNode(2, 11, 'FUNC',
                        Token(TokenType.FUNC, 'func', 2, 12),
                        ListNode(2, 17, 'PARAM',
                            Token(TokenType.PARAM, 'param', 2, 18),
                            Token(TokenType.NUM_TYPE, 'i32', 2, 24),
                            Token(TokenType.NUM_TYPE, 'i32', 2, 28),
                            Token(TokenType.NUM_TYPE, 'i32', 2, 32)
                        )
                    )
                )
            )
        )

    def test_unexpected_after_val_types(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/result/unexpected_after_val_types.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:36: unexpected 'loop'")

    def test_unexpected_2(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/func/unexpected.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:32: unexpected 'if'")

    def test_unexpected_in_inner_type_sexp(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/func/unexpected_in_inner_type_sexp.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:19: unexpected 'i32'")

    def test_inner_type_sexp_not_present(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/func/inner_type_sexp_not_present.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    ListNode(2, 11, 'LOCAL',
                        Token(TokenType.LOCAL, 'local', 2, 12)
                    ),
                    ListNode(2, 19, 'NOP',
                        Token(TokenType.NOP, 'nop', 2, 20)
                    )
                )
            )
        )

    def test_if_expr_with_else(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/expr/if_expr_with_else.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    Token(TokenType.NAME, '$a', 2, 11),
                    ListNode(2, 14, 'IF',
                        Token(TokenType.IF, 'if', 2, 15),
                        ListNode(2, 18, 'THEN',
                            Token(TokenType.THEN, 'then', 2, 19)
                        ),
                        ListNode(2, 25, 'ELSE',
                            Token(TokenType.ELSE, 'else', 2, 26)
                        )
                    )
                )
            )
        )

    def test_more_than_one_op_expr(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/expr/more_than_one_op_expr.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    ListNode(2, 11, 'CALL',
                        Token(TokenType.CALL, 'call', 2, 12),
                        Token(TokenType.NAT, '4', 2, 17),
                        ListNode(2, 19, 'DROP',
                            Token(TokenType.DROP, 'drop', 2, 20),
                            ListNode(2, 25, 'LOCAL_INSTR',
                                Token(TokenType.LOCAL_INSTR, 'local.get', 2, 26),
                                Token(TokenType.NAME, '$a', 2, 36)
                            )
                        )
                    )
                )
            )
        )

    def test_nested_block(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/expr/nested_block.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    ListNode(2, 11, 'BLOCK',
                        Token(TokenType.BLOCK, 'block', 2, 12),
                        Token(TokenType.NAME, '$a', 2, 18),
                        ListNode(2, 21, 'RESULT',
                            Token(TokenType.RESULT, 'result', 2, 22)
                        ),
                        ListNode(2, 30, 'BLOCK',
                            Token(TokenType.BLOCK, 'block', 2, 31),
                            Token(TokenType.NAME, '$b', 2, 37),
                            ListNode(2, 40, 'RESULT',
                                Token(TokenType.RESULT, 'result', 2, 41),
                            )
                        )
                    )
                )
            )
        )

    def test_nested_if(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/expr/nested_if.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    Token(TokenType.NAME, '$a', 2, 11),
                    ListNode(2, 14, 'IF',
                        Token(TokenType.IF, 'if', 2, 15),
                        ListNode(2, 18, 'THEN',
                            Token(TokenType.THEN, 'then', 2, 19),
                            ListNode(2, 24, 'IF',
                                Token(TokenType.IF, 'if', 2, 25),
                                ListNode(2, 28, 'THEN',
                                    Token(TokenType.THEN, 'then', 2, 29)
                                )
                            )
                        ),
                        ListNode(2, 37, 'ELSE',
                            Token(TokenType.ELSE, 'else', 2, 38)
                        )
                    )
                )
            )
        )

    def test_nested_if_in_else_clause(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/expr/nested_if_in_else_clause.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    Token(TokenType.NAME, '$a', 2, 11),
                    ListNode(2, 14, 'IF',
                        Token(TokenType.IF, 'if', 2, 15),
                        ListNode(2, 18, 'THEN',
                            Token(TokenType.THEN, 'then', 2, 19),
                        ),
                        ListNode(2, 25, 'ELSE',
                            Token(TokenType.ELSE, 'else', 2, 26),
                            ListNode(2, 31, 'IF',
                                Token(TokenType.IF, 'if', 2, 32),
                                ListNode(2, 35, 'THEN',
                                    Token(TokenType.THEN, 'then', 2, 36)
                                )
                            )
                        )
                    )
                )
            )
        )

    def test_one_op_expr(self):
        self.assertEqual(
            parse(tokenize(read('parser_test_cases/expr/one_op_expr.wat'))),
            ListNode(1, 1, 'MODULE',
                Token(TokenType.MODULE, 'module', 1, 2),
                ListNode(2, 5, 'FUNC',
                    Token(TokenType.FUNC, 'func', 2, 6),
                    Token(TokenType.NAME, '$a', 2, 11),
                    ListNode(2, 14, 'LOCAL_INSTR',
                        Token(TokenType.LOCAL_INSTR, 'local.set', 2, 15),
                        Token(TokenType.NAT, '3', 2, 25)
                    )
                )
            )
        )

    def test_then_clause_not_present(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/expr/then_clause_not_present.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:19: unexpected 'else'")

    def test_unexpected_in_block_expr(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/expr/unexpected_in_block_expr.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:21: unexpected 'loop'")

    def test_unexpected_in_else_clause(self):
        with self.assertRaises(ParserError) as ctx:
            parse(tokenize(read('parser_test_cases/expr/unexpected_in_else_clause.wat')))

        self.assertEqual(str(ctx.exception), "Syntax error at 2:31: unexpected 'loop'")


if __name__ == '__main__':
    unittest.main()
