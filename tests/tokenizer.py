import unittest
from wafunextr.token import Token
from wafunextr.token_type import TokenType
from wafunextr.tokenizer import tokenize


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
                Token(TokenType.LPAR, '('),
                Token(TokenType.MODULE, 'module'),
                Token(TokenType.RPAR, ')')
            ]
        )

    def test_line_comment_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('line_comment_module.wat')),
            [
                Token(TokenType.LPAR, '('),
                Token(TokenType.MODULE, 'module'),
                Token(TokenType.RPAR, ')')
            ]
        )

    def test_multiline_comment_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('multiline_comment_module.wat')),
            [
                Token(TokenType.LPAR, '('),
                Token(TokenType.MODULE, 'module'),
                Token(TokenType.RPAR, ')')
            ]
        )

    def test_add_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('add.wat')),
            [
                Token(TokenType.LPAR, '('),
                Token(TokenType.MODULE, 'module'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.FUNC, 'func'),
                Token(TokenType.NAME, '$add'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.PARAM, 'param'),
                Token(TokenType.NAME, '$a'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.PARAM, 'param'),
                Token(TokenType.NAME, '$b'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.RESULT, 'result'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.INT_INSTR, 'i32.add'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.LOCAL_INSTR, 'local.get'),
                Token(TokenType.NAME, '$a'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.LOCAL_INSTR, 'local.get'),
                Token(TokenType.NAME, '$b'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')')
            ]
        )

    def test_if_module(self):
        self.assertEqual(
            tokenize(TokenizerTest.read('if.wat')),
            [
                Token(TokenType.LPAR, '('),
                Token(TokenType.MODULE, 'module'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.FUNC, 'func'),
                Token(TokenType.NAME, '$ifexpr'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.PARAM, 'param'),
                Token(TokenType.NAME, '$n'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.PARAM, 'param'),
                Token(TokenType.NAME, '$control'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.RESULT, 'result'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.INT_INSTR, 'i32.add'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.LOCAL_INSTR, 'local.get'),
                Token(TokenType.NAME, '$n'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.IF, 'if'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.RESULT, 'result'),
                Token(TokenType.NUM_TYPE, 'i32'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.INT_INSTR, 'i32.ge_s'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.LOCAL_INSTR, 'local.get'),
                Token(TokenType.NAME, '$control'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.CONST_INSTR, 'i32.const'),
                Token(TokenType.NAT, '0'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.THEN, 'then'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.CONST_INSTR, 'i32.const'),
                Token(TokenType.NAT, '1'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.ELSE, 'else'),
                Token(TokenType.LPAR, '('),
                Token(TokenType.CONST_INSTR, 'i32.const'),
                Token(TokenType.NUM, '-1'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')'),
                Token(TokenType.RPAR, ')')
            ]
        )


if __name__ == '__main__':
    unittest.main()
