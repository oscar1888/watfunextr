## Grammar of WebAssembly Text modules used in `watfunextr`
This file contains a subset of the **WebAssembly Text (WAT)** grammar used in `watfunextr`.
Some production rules were not considered in order to simplify the complexity of the project. 
The idea behind choosing a subset of the original grammar is to make a WAT module appear as a single s-expression.

```
<module> ::= '(' 'module' <NAME>? <module_field>* ')'

<module_field> ::= <typedef>
                |  <func>
                |  <global>
                |  <export>

<export> ::= '(' 'export' <STRING> <exkind> ')'
<exkind> ::= '(' ('func'|'global') <var> ')'

<global> ::= '(' 'global' <NAME>? <global_type> <instr>* ')'

<global_type>::= <val_type>
              |  '(' 'mut' <val_type> ')'

<typedef> ::= '(' 'type' <NAME>? '(' 'func' <param>* <result>* ')' ')'

<param> ::= '(' 'param' <val_type>* ')'
         |  '(' 'param' <NAME> <val_type> ')'

<val_type> ::= <NUM_TYPE>

<result> ::= '(' 'result' <val_type>* ')'

<func> ::= '(' 'func' <NAME>? <func_type> <local>* <instr>* ')'

<func_type> ::= ('(' 'type' <var> ')')? <param>* <result>*

<var> ::= <NAT> | <NAME>

<local> ::= '(' 'local' <val_type>* ')'
         |  '(' 'local' <NAME> <val_type> ')'

<instr> ::= <expr>
         |  <op>

<expr> ::= '(' <op> <expr>* ')'
        |  '(' 'block' <NAME>? <result>? <instr>* ')'
        |  '(' 'loop' <NAME>? <result>? <instr>* ')'
        |  '(' 'if' <NAME>? <result>? <expr>* '(' 'then' <instr>* ')' ('(' 'else' <instr>* ')')? ')'

<op> ::= 'unreachable'
      |  'nop'
      |  'br' <var>
      |  'br_if' <var>
      |  'return'
      |  'call' <var>
      |  'drop'
      |  'select'
      |  'local.get' <var>
      |  'local.set' <var>
      |  'local.tee' <var>
      |  'global.get' <var>
      |  'global.set' <var>
      |  <CONST_INSTR> (<NUM> | <NAT>)
      |  <INT_INSTR>
      |  <FLOAT_INSTR>
```

### Information about tokens:
```
<NAME>: $(<LETTER> | <DIGIT> | '_' | '.' | '+' | '-' | '*' | '/' | '\' | '^' | '~' | '=' | '<' | '>' | '!' | '?' | '@' | '#' | '$' | '%' | '&' | '|' | ':' | ''' | '`')+
<NUM_TYPE>: 'i32' | 'i64' | 'f32' | 'f64'
<NUM>: <INT> | <FLOAT>
<NAT>: integers without sign prefix
<INT>: integers with sign prefix
<CONST_INSTR>, <INT_INSTR> e <FLOAT_INSTR> are instructions of constant (e.g. i32.const), int (e.g. i32.add) and float (e.g. f64.sub) respectively.
```

For more details on the included tokens, check the `watfunextr/tokenizer/token_patterns.py` file.
