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
    GLOBAL_INSTR = 17

    # Keywords
    MODULE = 18
    TYPE = 19
    FUNC = 20
    PARAM = 21
    RESULT = 22
    LOCAL = 23
    BLOCK = 24
    LOOP = 25
    IF = 26
    THEN = 27
    ELSE = 28
    MUT = 29
    GLOBAL = 30
    EXPORT = 31

    # Values
    NAME = 32
    NAT = 33
    NUM = 34
    NUM_TYPE = 35
    STRING = 36
