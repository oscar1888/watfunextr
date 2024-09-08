from enum import Enum


class TokenType(Enum):
    # Separators
    WHITESPACE = 1
    COMMENT = 2
    LPAR = 3
    RPAR = 4

    # Operations
    UNREACHABLE = 5
    NOP = 6
    BR = 7
    BR_IF = 8
    RETURN = 9
    CALL = 10
    DROP = 11
    SELECT = 12
    LOCAL_INSTR = 13
    CONST_INSTR = 14
    INT_INSTR = 15
    FLOAT_INSTR = 16

    # Keywords
    MODULE = 17
    TYPE = 18
    FUNC = 19
    PARAM = 20
    RESULT = 21
    LOCAL = 22
    BLOCK = 23
    LOOP = 24
    IF = 25
    THEN = 26
    ELSE = 27

    # Values
    NAME = 28
    NAT = 29
    NUM = 30
    NUM_TYPE = 31
