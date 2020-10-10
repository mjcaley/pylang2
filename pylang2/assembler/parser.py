from lark import Lark

grammar = r"""
    start : (struct | definition | function)*

    struct : "struct" CNAME types
    types: (_int | _float | _str)+

    definition : "define" CNAME "=" _operand
    
    function : "func" CNAME "locals" "=" INT "," "args" "=" INT statements
    
    statements : _statement+
    _statement : nullary_instruction | unary_instruction | label
    nullary_instruction : (HALT | NOOP
                        | ADD | SUB | MUL | DIV | MOD
                        | POP
                        | JMP | JMPT | JMPF
                        | TESTEQ | TESTNE | TESTLT | TESTGT
                        | CALLVIRT | RET)
    unary_instruction : (LDCONST | LDLOCAL | STLOCAL
                      | CALLFUNC
                      | NEWSTRUCT | LDFIELD | STFIELD
                      | NEWARRAY | LDELEM | STELEM) _operand
    label: CNAME ":"
    
    HALT : "halt"
    NOOP : "noop"
    ADD : "add"
    SUB : "sub"
    MUL : "mul"
    DIV : "div"
    MOD : "mod"
    LDCONST : "ldconst"
    LDLOCAL : "ldlocal"
    STLOCAL : "stlocal"
    POP : "pop"
    TESTEQ : "testeq"
    TESTNE : "testne"
    TESTLT : "testlt"
    TESTGT : "testgt"
    JMP : "jmp"
    JMPT : "jmpt"
    JMPF : "jmpf"
    CALLFUNC : "callfunc"
    CALLVIRT : "callvirt"
    RET : "ret"
    NEWSTRUCT : "newstruct"
    LDFIELD : "ldfield"
    STFIELD : "stfield"
    NEWARRAY : "newarray"
    LDELEM : "ldelem"
    STELEM : "stelem"
    
    _operand : int_operand
            | float_operand
            | str_operand
            | binding
    int_operand : SIGNED_INT _int?
    float_operand : SIGNED_FLOAT _float
    str_operand : ESCAPED_STRING STR? 
    
    _int : I8 | I16 | I32 | I64 | U8 | U16 | U32 | U64 | ADDR
    _float : F32 | F64
    _str : STR
    binding : CNAME
    
    I8 : "i8"
    I16 : "i16"
    I32 : "i32"
    I64 : "i64"
    U8 : "u8"
    U16 : "u16"
    U32 : "u32"
    U64 : "u64"
    F32 : "f32"
    F64 : "f64"
    ADDR : "addr"
    STR : "str"
    
    %import common.ESCAPED_STRING
    %import common.SIGNED_FLOAT
    %import common.SIGNED_INT
    %import common.INT
    %import common.CNAME
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, parser="lalr")
