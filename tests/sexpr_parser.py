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


if __name__ == '__main__':
    unittest.main()
