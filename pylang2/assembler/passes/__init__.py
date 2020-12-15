"""Compiler passes

to_ast - parse tree to AST
check redefinitions
check undefined bindings
check definition cycles
to_symbol_table - creates symbol table and constant set
calculate addresses - writes addresses on
bindings_to_constants - bindings replaced by symbol values
    ConstantSymbol -> Constant
    FunctionSymbol -> Constant (int32) from address
    StructSymbol -> Constant (int32)  from struct index
    LabelSymbol -> Constant (int32) from address
check valid locals and args
code generation
"""