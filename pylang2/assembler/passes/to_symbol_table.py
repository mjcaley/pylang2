from functools import singledispatchmethod

from ..ast import (
    Constant,
    Type,
    ASTRoot,
    ASTDefinition,
    ASTStruct,
    ASTFunction,
    ASTLabel,
    ASTSymbolTableRoot,
    Symbol,
    ConstantSymbol,
    FunctionSymbol,
    StructSymbol,
    LabelSymbol,
    ASTSymbolFunction,
    ASTUnaryInstruction,
    ASTOperand,
)


class ToSymbolTableAST:
    def __init__(self):
        self.symbols: dict[str, Symbol] = dict()
        self.constants: set[Constant] = set()

    @staticmethod
    def run_pass(tree):
        to_symbol_table_ast = ToSymbolTableAST()
        new_tree = to_symbol_table_ast.transform(tree)

        return new_tree

    @singledispatchmethod
    def transform(self, arg):
        return arg

    @transform.register
    def _(self, root: ASTRoot):
        functions = []
        for child in root.children:
            node = self.transform(child)
            if node is not None:
                functions.append(node)

        return ASTSymbolTableRoot(self.symbols, self.constants, functions)

    @transform.register
    def _(self, definition: ASTDefinition):
        constant = definition.operand.value
        self.transform(constant)
        self.symbols[definition.name] = ConstantSymbol(constant)

    @transform.register
    def _(self, struct: ASTStruct):
        name = Constant(Type.String, struct.name)
        self.constants.add(name)

        types = [self.transform(t) for t in struct.types if t is not None]
        self.symbols[struct.name] = StructSymbol(name, types)

    @transform.register
    def _(self, function: ASTFunction):
        name = Constant(Type.String, function.name)
        self.transform(name)
        self.symbols[function.name] = FunctionSymbol(
            name, function.num_locals, function.num_args
        )

        statements = [
            self.transform(statement)
            for statement in function.statements
            if statement is not None
        ]

        return ASTSymbolFunction(function.name, statements)

    @transform.register
    def _(self, label: ASTLabel):

        self.symbols[label.name] = LabelSymbol()

    @transform.register
    def _(self, unary: ASTUnaryInstruction):
        self.transform(unary.operand)

        return unary

    @transform.register
    def _(self, operand: ASTOperand):
        self.transform(operand.value)

        return operand

    @transform.register
    def _(self, constant: Constant):
        if constant.type_ in (Type.UInt64, Type.Int64, Type.Float64, Type.String, Type.Address):
            self.constants.add(constant)

        return constant
