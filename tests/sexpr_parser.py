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
            parse(tokenize(read('simple_module.wat'))),
            ListNode(
                'Program',
                ListNode(
                    'List',
                    Token(TokenType.MODULE, 'module', 1, 2)
                )
            )
        )

    def test_add_module(self):
        self.assertEqual(
            parse(tokenize(read('add.wat'))),
            ListNode(
                'Program',
                ListNode(
                    'List',
                    Token(TokenType.MODULE, 'module', 1, 2),
                    ListNode(
                        'List',
                        Token(TokenType.FUNC, 'func', 3, 6),
                        Token(TokenType.NAME, '$add', 3, 11),
                        ListNode(
                            'List',
                            Token(TokenType.PARAM, 'param', 3, 17),
                            Token(TokenType.NAME, '$a', 3, 23),
                            Token(TokenType.NUM_TYPE, 'i32', 3, 26)
                        ),
                        ListNode(
                            'List',
                            Token(TokenType.PARAM, 'param', 3, 32),
                            Token(TokenType.NAME, '$b', 3, 38),
                            Token(TokenType.NUM_TYPE, 'i32', 3, 41)
                        ),
                        ListNode(
                            'List',
                            Token(TokenType.RESULT, 'result', 3, 47),
                            Token(TokenType.NUM_TYPE, 'i32', 3, 54)
                        ),
                        ListNode(
                            'List',
                            Token(TokenType.INT_INSTR, 'i32.add', 4, 10),
                            ListNode(
                                'List',
                                Token(TokenType.LOCAL_INSTR, 'local.get', 4, 19),
                                Token(TokenType.NAME, '$a', 4, 29)
                            ),
                            ListNode(
                                'List',
                                Token(TokenType.LOCAL_INSTR, 'local.get', 4, 34),
                                Token(TokenType.NAME, '$b', 4, 44)
                            )
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
            parse(tokenize(read('exceeding_right_par.wat')))

        self.assertEqual(str(ctx.exception), 'Syntax error at 3:2: unexpected right parenthesis')


if __name__ == '__main__':
    unittest.main()
