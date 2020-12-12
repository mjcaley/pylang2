from functools import singledispatchmethod

from ..ast import ASTSymbolTableRoot, ASTSymbolFunction, ASTUnaryInstruction, ASTOperand


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
        constant = self.symbols[arg].constant

        return constant
