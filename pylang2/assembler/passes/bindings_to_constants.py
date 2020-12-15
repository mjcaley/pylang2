from functools import singledispatchmethod

from ..ast import ASTSymbolTableRoot, ASTSymbolFunction, ASTUnaryInstruction, ASTOperand, FunctionSymbol, LabelSymbol, StructSymbol, ConstantSymbol, Constant, Type


class BindingsToConstants:
    """Converts operand bindings to constants.

    Assumes that all definitions were resolved to constants.
    """

    def __init__(self):
        self.symbols = {}

    @staticmethod
    def run_pass(tree):
        b = BindingsToConstants()
        new_tree = b.transform(tree)

        return new_tree

    @singledispatchmethod
    def transform(self, arg):
        return arg

    @transform.register
    def _(self, arg: ASTSymbolTableRoot):
        self.symbols = arg.symbol_table
        arg.functions = self.transform([self.transform(function) for function in arg.functions])

        return arg

    @transform.register
    def _(self, arg: ASTSymbolFunction):
        arg.statements = [self.transform(statement) for statement in arg.statements]

        return arg

    @transform.register
    def _(self, arg: ASTUnaryInstruction):
        arg.operand = self.transform(arg.operand)

        return arg

    @transform.register
    def _(self, arg: ASTOperand):
        arg.value = self.transform(arg.value)

        return arg

    @transform.register
    def _(self, arg: str):
        # TODO: This assumes it's a constant, where it can be any symbol
        constant = self.transform(self.symbols[arg])

        return constant

    @transform.register
    def _(self, arg: ConstantSymbol):
        # TODO: If Int64 or Float64 needs constant index defined
        return arg.constant

    @transform.register
    def _(self, arg: FunctionSymbol):
        return Constant(Type.Int32, arg.address)

    @transform.register
    def _(self, arg: StructSymbol):
        # TODO: Struct index needs to be defined
        return Constant(Type.Int32, 0)

    @transform.register
    def _(self, arg: LabelSymbol):
        return Constant(Type.Int32, arg.address)
