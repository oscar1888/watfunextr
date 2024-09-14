import unittest
from wafunextr.tokenizer.token import Token
from wafunextr.tokenizer.token_type import TokenType
from wafunextr.tokenizer import tokenize
from wafunextr.tokenizer.tokenizer_error import TokenizerError


class TokenizerTest(unittest.TestCase):

    @staticmethod
    def read(file_name: str) -> str:
        complete_path: str = './example_modules/' + file_name
        try:
            with open(complete_path) as f:
                return f.read()
        except OSError:
            print(f'Could not open file at: {complete_path}')

    def test_simple_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('simple_module.wat')),
            [
                Token(TokenType.LPAR, '(', 1),
                Token(TokenType.MODULE, 'module', 1),
                Token(TokenType.RPAR, ')', 1)
            ]
        )

    def test_line_comment_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('line_comment_module.wat')),
            [
                Token(TokenType.LPAR, '(', 1),
                Token(TokenType.MODULE, 'module', 1),
                Token(TokenType.RPAR, ')', 2)
            ]
        )

    def test_multiline_comment_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('multiline_comment_module.wat')),
            [
                Token(TokenType.LPAR, '(', 1),
                Token(TokenType.MODULE, 'module', 1),
                Token(TokenType.RPAR, ')', 10)
            ]
        )

    def test_add_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('add.wat')),
            [
                Token(TokenType.LPAR, '(', 1),
                Token(TokenType.MODULE, 'module', 1),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.FUNC, 'func', 3),
                Token(TokenType.NAME, '$add', 3),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.PARAM, 'param', 3),
                Token(TokenType.NAME, '$a', 3),
                Token(TokenType.NUM_TYPE, 'i32', 3),
                Token(TokenType.RPAR, ')', 3),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.PARAM, 'param', 3),
                Token(TokenType.NAME, '$b', 3),
                Token(TokenType.NUM_TYPE, 'i32', 3),
                Token(TokenType.RPAR, ')', 3),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.RESULT, 'result', 3),
                Token(TokenType.NUM_TYPE, 'i32', 3),
                Token(TokenType.RPAR, ')', 3),
                Token(TokenType.LPAR, '(', 4),
                Token(TokenType.INT_INSTR, 'i32.add', 4),
                Token(TokenType.LPAR, '(', 4),
                Token(TokenType.LOCAL_INSTR, 'local.get', 4),
                Token(TokenType.NAME, '$a', 4),
                Token(TokenType.RPAR, ')', 4),
                Token(TokenType.LPAR, '(', 4),
                Token(TokenType.LOCAL_INSTR, 'local.get', 4),
                Token(TokenType.NAME, '$b', 4),
                Token(TokenType.RPAR, ')', 4),
                Token(TokenType.RPAR, ')', 4),
                Token(TokenType.RPAR, ')', 5),
                Token(TokenType.RPAR, ')', 6)
            ]
        )

    def test_if_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('if.wat')),
            [
                Token(TokenType.LPAR, '(', 1),
                Token(TokenType.MODULE, 'module', 1),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.FUNC, 'func', 3),
                Token(TokenType.NAME, '$ifexpr', 3),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.PARAM, 'param', 3),
                Token(TokenType.NAME, '$n', 3),
                Token(TokenType.NUM_TYPE, 'i32', 3),
                Token(TokenType.RPAR, ')', 3),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.PARAM, 'param', 3),
                Token(TokenType.NAME, '$control', 3),
                Token(TokenType.NUM_TYPE, 'i32', 3),
                Token(TokenType.RPAR, ')', 3),
                Token(TokenType.LPAR, '(', 3),
                Token(TokenType.RESULT, 'result', 3),
                Token(TokenType.NUM_TYPE, 'i32', 3),
                Token(TokenType.RPAR, ')', 3),
                Token(TokenType.LPAR, '(', 4),
                Token(TokenType.INT_INSTR, 'i32.add', 4),
                Token(TokenType.LPAR, '(', 5),
                Token(TokenType.LOCAL_INSTR, 'local.get', 5),
                Token(TokenType.NAME, '$n', 5),
                Token(TokenType.RPAR, ')', 5),
                Token(TokenType.LPAR, '(', 6),
                Token(TokenType.IF, 'if', 6),
                Token(TokenType.LPAR, '(', 6),
                Token(TokenType.RESULT, 'result', 6),
                Token(TokenType.NUM_TYPE, 'i32', 6),
                Token(TokenType.RPAR, ')', 6),
                Token(TokenType.LPAR, '(', 7),
                Token(TokenType.INT_INSTR, 'i32.ge_s', 7),
                Token(TokenType.LPAR, '(', 7),
                Token(TokenType.LOCAL_INSTR, 'local.get', 7),
                Token(TokenType.NAME, '$control', 7),
                Token(TokenType.RPAR, ')', 7),
                Token(TokenType.LPAR, '(', 7),
                Token(TokenType.CONST_INSTR, 'i32.const', 7),
                Token(TokenType.NAT, '0', 7),
                Token(TokenType.RPAR, ')', 7),
                Token(TokenType.RPAR, ')', 7),
                Token(TokenType.LPAR, '(', 8),
                Token(TokenType.THEN, 'then', 8),
                Token(TokenType.LPAR, '(', 8),
                Token(TokenType.CONST_INSTR, 'i32.const', 8),
                Token(TokenType.NAT, '1', 8),
                Token(TokenType.RPAR, ')', 8),
                Token(TokenType.RPAR, ')', 8),
                Token(TokenType.LPAR, '(', 9),
                Token(TokenType.ELSE, 'else', 9),
                Token(TokenType.LPAR, '(', 9),
                Token(TokenType.CONST_INSTR, 'i32.const', 9),
                Token(TokenType.NUM, '-1', 9),
                Token(TokenType.RPAR, ')', 9),
                Token(TokenType.RPAR, ')', 9),
                Token(TokenType.RPAR, ')', 10),
                Token(TokenType.RPAR, ')', 11),
                Token(TokenType.RPAR, ')', 12),
                Token(TokenType.RPAR, ')', 13)
            ]
        )

    def test_unexpected_token_module_1(self):

        with self.assertRaises(TokenizerError) as ctx:
            tokenize(TokenizerTest.read('unexpected_token.wat'))

        self.assertEqual(str(ctx.exception), 'Unexpected token at line 2: funz')

    def test_unexpected_token_module_2(self):

        with self.assertRaises(TokenizerError) as ctx:
            tokenize(TokenizerTest.read('unexpected_token_2.wat'))

        self.assertEqual(str(ctx.exception), 'Unexpected token at line 3: extra')


if __name__ == '__main__':
    unittest.main()
