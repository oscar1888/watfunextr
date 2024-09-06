Digit = '[0-9]'
HexDigit = '[0-9a-fA-F]'
Num = Digit + '(_?' + Digit + ')*'
HexNum = HexDigit + '(_?' + HexDigit + ')*'
Nat = Num + '|' + '0x' + HexNum

Sign = r'\+|-'
Int = '(' + Sign + ')' + Nat

Frac = Num
HexFrac = HexNum
Float = \
    '(' + Sign + ')' + '?' + Num + r'\.' + '(' + Frac + ')' + '?' + \
    '|' + '(' + Sign + ')' + '?' + Num + r'(\.' + '(' + Frac + ')' + '?' + ')?' + '(e|E)' + '(' + Sign + ')' + '?' + Num + \
    '|' + '(' + Sign + ')' + '?' + '0x' + HexNum + r'\.' + '(' + HexFrac + ')' + '?' + \
    '|' + '(' + Sign + ')' + '?' + '0x' + HexNum + r'(\.' + '(' + HexFrac + ')' + '?' + ')?' + '(p|P)' + '(' + Sign + ')' + '?' + Num + \
    '|' + '(' + Sign + ')' + '?' + 'inf' + \
    '|' + '(' + Sign + ')' + '?' + 'nan' + \
    '|' + '(' + Sign + ')' + '?' + 'nan:' + '0x' + HexNum

Letter = '[a-zA-Z]'
Symbol = \
    r'\.' + \
    '|' + r'\+' + \
    '|' + '-' + \
    '|' + r'\*' + \
    '|' + r'\/' + \
    '|' + r'\\' + \
    '|' + r'\^' + \
    '|' + r'\~' + \
    '|' + '=' + \
    '|' + '<' + \
    '|' + '>' + \
    '|' + '!' + \
    '|' + r'\?' + \
    '|' + '@' + \
    '|' + '#' + \
    '|' + r'\$' + \
    '|' + '%' + \
    '|' + '&' + \
    '|' + r'\|' + \
    '|' + ':' + \
    '|' + '′' + \
    '|' + '`'
Name = r'\$' + '(' + Letter + '|' + Digit + '|' + '_' + '|' + '(' + Symbol + ')' + ')+'

IXX = 'i' + '(' + '32' + '|' + '64' + ')'
FXX = 'f' + '(' + '32' + '|' + '64' + ')'
NXX = IXX + '|' + FXX

SIGN = 's' + '|' + 'u'
INT_GEN_INSTR = IXX + r'\.(' + \
                'clz' + \
                '|' + 'ctz' + \
                '|' + 'popcnt' + \
                '|' + 'add' + \
                '|' + 'sub' + \
                '|' + 'mul' + \
                '|' + 'div_(' + SIGN + ')' + \
                '|' + 'rem_(' + SIGN + ')' + \
                '|' + 'and' + \
                '|' + 'or' + \
                '|' + 'xor' + \
                '|' + 'shl' + \
                '|' + 'shr_(' + SIGN + ')' + \
                '|' + 'rotl' + \
                '|' + 'rotr' + \
                \
                '|' + 'eqz' + \
                '|' + 'eq' + \
                '|' + 'ne' + \
                '|' + 'lt_(' + SIGN + ')' + \
                '|' + 'gt_(' + SIGN + ')' + \
                '|' + 'le_(' + SIGN + ')' + \
                '|' + 'ge_(' + SIGN + ')' \
                + ')'

I32_CONV = r'i32\.(' + \
           'wrap_i64' + \
           '|' + 'trunc(_sat)?_(' + FXX + ')_(' + SIGN + ')' + \
           '|' + 'reinterpret_f32' + \
           '|' + 'extend(8|16)_s' \
           + ')'

I64_CONV = r'i64\.(' + \
           'extend_i32_(' + SIGN + ')' + \
           '|' + 'trunc(_sat)?_(' + FXX + ')_(' + SIGN + ')' + \
           '|' + 'reinterpret_f64' + \
           '|' + 'extend(8|16|32)_s' \
           + ')'

F32_CONV = r'f32\.(' + \
           'convert_(' + IXX + ')_(' + SIGN + ')' + \
           '|' + 'demote_f64' + \
           '|' + 'reinterpret_i32' \
           + ')'

F64_CONV = r'f64\.(' + \
           'convert_(' + IXX + ')_(' + SIGN + ')' + \
           '|' + 'promote_f32' + \
           '|' + 'reinterpret_i64' \
           + ')'

FLOAT_GEN_INSTR = FXX + r'\.(' + \
              'abs' + \
              '|' + 'neg' + \
              '|' + 'ceil' + \
              '|' + 'floor' + \
              '|' + 'trunc' + \
              '|' + 'nearest' + \
              '|' + 'sqrt' + \
              '|' + 'add' + \
              '|' + 'sub' + \
              '|' + 'mul' + \
              '|' + 'div' + \
              '|' + 'min' + \
              '|' + 'max' + \
              '|' + 'copysign' + \
              \
              '|' + 'eq' + \
              '|' + 'ne' + \
              '|' + 'lt' + \
              '|' + 'gt' + \
              '|' + 'le' + \
              '|' + 'ge' \
              + ')'

FLOAT_INSTR = '(' + F32_CONV + ')' + '|' + '(' + F64_CONV + ')' + '|' + '(' + FLOAT_GEN_INSTR + ')'
INT_INSTR = '(' + I32_CONV + ')' + '|' + '(' + I64_CONV + ')' + '|' + '(' + INT_GEN_INSTR + ')'

token_patterns = {
    # Separators
    'SPACE': r'[ \t\r\n]',
    'COMMENT': r'\(;' + '.*?' + r';\)' + '|' + ';;' + '.*?' + r'\n',
    'LPAR': r'\(',
    'RPAR': r'\)',

    # Operations
    'UNREACHABLE': 'unreachable',
    'NOP': 'nop',
    'BR': 'br',
    'BR_IF': 'br_if',
    'RETURN': 'return',
    'CALL': 'call',
    'DROP': 'drop',
    'SELECT': 'select',
    'LOCAL_INSTR': 'local' + r'\.(' + 'get' + '|' + 'set' + '|' + 'tee' ')',
    'CONST_INSTR': NXX + r'\.const',
    'INT_INSTR': INT_INSTR,
    'FLOAT_INSTR': FLOAT_INSTR,

    # Keywords
    'MODULE': 'module',
    'TYPE': 'type',
    'FUNC': 'func',
    'PARAM': 'param',
    'RESULT': 'result',
    'LOCAL': 'local',
    'BLOCK': 'block',
    'LOOP': 'loop',
    'IF': 'if',
    'THEN': 'then',
    'ELSE': 'else',

    # Values
    'NAME': Name,
    'NAT': Nat,
    'NUM': '(' + Int + ')' + '|' + '(' + Float + ')',
    'NUM_TYPE': NXX,
}
