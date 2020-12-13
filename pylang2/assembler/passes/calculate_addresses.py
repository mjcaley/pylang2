from functools import singledispatchmethod

from ..ast import ASTSymbolTableRoot, ASTSymbolFunction, ASTLabel, ASTNullaryInstruction, ASTUnaryInstruction


class CalculateAddresses:
    def __init__(self, symbols):
        self.symbols = symbols
        self.current_address = 0

    @staticmethod
    def run_pass(tree):
        c = CalculateAddresses(tree.symbol_table)
        c.transform(tree)

        return tree

    @singledispatchmethod
    def transform(self, arg):
        return

    @transform.register
    def _(self, arg: ASTSymbolTableRoot):
        for function in arg.functions:
            self.transform(function)
        arg.symbol_table = self.symbols

        return arg

    @transform.register
    def _(self, arg: ASTSymbolFunction):
        self.symbols[arg.name].address = self.current_address
        for statement in arg.statements:
            self.transform(statement)

    @transform.register
    def _(self, arg: ASTLabel):
        self.symbols[arg.name].address = self.current_address

    @transform.register
    def _(self, _: ASTNullaryInstruction):
        self.current_address += 1

    @transform.register
    def _(self, _: ASTUnaryInstruction):
        self.current_address += 5
