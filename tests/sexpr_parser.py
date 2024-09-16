import unittest

from tests.utils import read
from wafunextr.parser import parse
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


if __name__ == '__main__':
    unittest.main()
