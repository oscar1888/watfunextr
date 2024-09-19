import unittest

from tests.utils import read
from watfunextr.tokenizer.token import Token
from watfunextr.tokenizer.token_type import TokenType
from watfunextr.tokenizer import tokenize
from watfunextr.tokenizer.tokenizer_error import TokenizerError


class TokenizerTest(unittest.TestCase):

    def test_simple_module(self):
        self.assertEqual(
            tokenize(read('misc/simple_module.wat')),
            [
                Token(TokenType.LPAR, '(', 1, 1),
                Token(TokenType.MODULE, 'module', 1, 2),
                Token(TokenType.RPAR, ')', 1, 8)
            ]
        )

    def test_line_comment_module(self):
        self.assertEqual(
            tokenize(read('tokenizer_test_cases/line_comment_module.wat')),
            [
                Token(TokenType.LPAR, '(', 1, 1),
                Token(TokenType.MODULE, 'module', 1, 2),
                Token(TokenType.RPAR, ')', 2, 1)
            ]
        )

    def test_multiline_comment_module(self):
        self.assertEqual(
            tokenize(read('tokenizer_test_cases/multiline_comment_module.wat')),
            [
                Token(TokenType.LPAR, '(', 1, 1),
                Token(TokenType.MODULE, 'module', 1, 2),
                Token(TokenType.RPAR, ')', 10, 1)
            ]
        )

    def test_add_module(self):
        self.assertEqual(
            tokenize(read('misc/add.wat')),
            [
                Token(TokenType.LPAR, '(', 1, 1),
                Token(TokenType.MODULE, 'module', 1, 2),
                Token(TokenType.LPAR, '(', 3, 5),
                Token(TokenType.FUNC, 'func', 3, 6),
                Token(TokenType.NAME, '$add', 3, 11),
                Token(TokenType.LPAR, '(', 3, 16),
                Token(TokenType.PARAM, 'param', 3, 17),
                Token(TokenType.NAME, '$a', 3, 23),
                Token(TokenType.NUM_TYPE, 'i32', 3, 26),
                Token(TokenType.RPAR, ')', 3, 29),
                Token(TokenType.LPAR, '(', 3, 31),
                Token(TokenType.PARAM, 'param', 3, 32),
                Token(TokenType.NAME, '$b', 3, 38),
                Token(TokenType.NUM_TYPE, 'i32', 3, 41),
                Token(TokenType.RPAR, ')', 3, 44),
                Token(TokenType.LPAR, '(', 3, 46),
                Token(TokenType.RESULT, 'result', 3, 47),
                Token(TokenType.NUM_TYPE, 'i32', 3, 54),
                Token(TokenType.RPAR, ')', 3, 57),
                Token(TokenType.LPAR, '(', 4, 9),
                Token(TokenType.INT_INSTR, 'i32.add', 4, 10),
                Token(TokenType.LPAR, '(', 4, 18),
                Token(TokenType.LOCAL_INSTR, 'local.get', 4, 19),
                Token(TokenType.NAME, '$a', 4, 29),
                Token(TokenType.RPAR, ')', 4, 31),
                Token(TokenType.LPAR, '(', 4, 33),
                Token(TokenType.LOCAL_INSTR, 'local.get', 4, 34),
                Token(TokenType.NAME, '$b', 4, 44),
                Token(TokenType.RPAR, ')', 4, 46),
                Token(TokenType.RPAR, ')', 4, 47),
                Token(TokenType.RPAR, ')', 5, 5),
                Token(TokenType.RPAR, ')', 6, 1)
            ]
        )

    def test_if_module(self):
        self.assertEqual(
            tokenize(read('misc/if.wat')),
            [
                Token(TokenType.LPAR, '(', 1, 1),
                Token(TokenType.MODULE, 'module', 1, 2),
                Token(TokenType.LPAR, '(', 3, 5),
                Token(TokenType.FUNC, 'func', 3, 6),
                Token(TokenType.NAME, '$ifexpr', 3, 11),
                Token(TokenType.LPAR, '(', 3, 19),
                Token(TokenType.PARAM, 'param', 3, 20),
                Token(TokenType.NAME, '$n', 3, 26),
                Token(TokenType.NUM_TYPE, 'i32', 3, 29),
                Token(TokenType.RPAR, ')', 3, 32),
                Token(TokenType.LPAR, '(', 3, 34),
                Token(TokenType.PARAM, 'param', 3, 35),
                Token(TokenType.NAME, '$control', 3, 41),
                Token(TokenType.NUM_TYPE, 'i32', 3, 50),
                Token(TokenType.RPAR, ')', 3, 53),
                Token(TokenType.LPAR, '(', 3, 55),
                Token(TokenType.RESULT, 'result', 3, 56),
                Token(TokenType.NUM_TYPE, 'i32', 3, 63),
                Token(TokenType.RPAR, ')', 3, 66),
                Token(TokenType.LPAR, '(', 4, 9),
                Token(TokenType.INT_INSTR, 'i32.add', 4, 10),
                Token(TokenType.LPAR, '(', 5, 13),
                Token(TokenType.LOCAL_INSTR, 'local.get', 5, 14),
                Token(TokenType.NAME, '$n', 5, 24),
                Token(TokenType.RPAR, ')', 5, 26),
                Token(TokenType.LPAR, '(', 6, 13),
                Token(TokenType.IF, 'if', 6, 14),
                Token(TokenType.LPAR, '(', 6, 17),
                Token(TokenType.RESULT, 'result', 6, 18),
                Token(TokenType.NUM_TYPE, 'i32', 6, 25),
                Token(TokenType.RPAR, ')', 6, 28),
                Token(TokenType.LPAR, '(', 7, 17),
                Token(TokenType.INT_INSTR, 'i32.ge_s', 7, 18),
                Token(TokenType.LPAR, '(', 7, 27),
                Token(TokenType.LOCAL_INSTR, 'local.get', 7, 28),
                Token(TokenType.NAME, '$control', 7, 38),
                Token(TokenType.RPAR, ')', 7, 46),
                Token(TokenType.LPAR, '(', 7, 48),
                Token(TokenType.CONST_INSTR, 'i32.const', 7, 49),
                Token(TokenType.NAT, '0', 7, 59),
                Token(TokenType.RPAR, ')', 7, 60),
                Token(TokenType.RPAR, ')', 7, 61),
                Token(TokenType.LPAR, '(', 8, 17),
                Token(TokenType.THEN, 'then', 8, 18),
                Token(TokenType.LPAR, '(', 8, 23),
                Token(TokenType.CONST_INSTR, 'i32.const', 8, 24),
                Token(TokenType.NAT, '1', 8, 34),
                Token(TokenType.RPAR, ')', 8, 35),
                Token(TokenType.RPAR, ')', 8, 36),
                Token(TokenType.LPAR, '(', 9, 17),
                Token(TokenType.ELSE, 'else', 9, 18),
                Token(TokenType.LPAR, '(', 9, 23),
                Token(TokenType.CONST_INSTR, 'i32.const', 9, 24),
                Token(TokenType.NUM, '-1', 9, 34),
                Token(TokenType.RPAR, ')', 9, 36),
                Token(TokenType.RPAR, ')', 9, 37),
                Token(TokenType.RPAR, ')', 10, 13),
                Token(TokenType.RPAR, ')', 11, 9),
                Token(TokenType.RPAR, ')', 12, 5),
                Token(TokenType.RPAR, ')', 13, 1)
            ]
        )

    def test_unexpected_token_module_1(self):

        with self.assertRaises(TokenizerError) as ctx:
            tokenize(read('tokenizer_test_cases/unexpected_token.wat'))

        self.assertEqual(str(ctx.exception), 'Unexpected token at 2:6: funz')

    def test_unexpected_token_module_2(self):

        with self.assertRaises(TokenizerError) as ctx:
            tokenize(read('tokenizer_test_cases/unexpected_token_2.wat'))

        self.assertEqual(str(ctx.exception), 'Unexpected token at 3:1: extra')

    def test_empty_module(self):

        with self.assertRaises(ValueError) as ctx:
            tokenize(read('tokenizer_test_cases/empty_program.wat'))

        self.assertEqual(str(ctx.exception), 'WAT program cannot be empty')


if __name__ == '__main__':
    unittest.main()
