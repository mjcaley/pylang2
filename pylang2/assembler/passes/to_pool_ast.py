"""Transforms symbol AST into a pool AST.


"""

from functools import singledispatchmethod

from ..ast import ASTSymbolTableRoot, FunctionSymbol, StructSymbol


class ToPoolAST:
    def __init__(self):
        self.constant_pool = []
        self.function_pool = []
        self.struct_pool = []

    @staticmethod
    def run_pass(tree):
        pass

    @singledispatchmethod
    def transform(self, arg):
        raise NotImplementedError

    @transform.register
    def _(self, arg: ASTSymbolTableRoot):
        self.constants = list(arg.constants)
        self.function_pool = [function for function in arg.symbol_table.values() if isinstance(function, FunctionSymbol)]
        self.symbols = list(struct for struct in arg.symbol_table.values() if isinstance(struct, StructSymbol))

        functions = [self.transform(function) for function in arg.functions]
        