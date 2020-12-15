from functools import singledispatchmethod

from ..ast import ASTSymbolTableRoot, ASTSymbolFunction, ASTUnaryInstruction, ASTOperand, FunctionSymbol, LabelSymbol, StructSymbol, ConstantSymbol, Constant, Type


class IndexSymbols:
    """Converts operand bindings to constants.

    Assumes that all definitions were resolved to constants.
    """

    def __init__(self):
        self.symbols = {}
        self.function_list = []
        self.struct_list = []
        self.constant_list = []

    def initialize(self):
        self.symbols = {}
        self.function_list = []
        self.struct_list = []
        self.constant_list = []

    @staticmethod
    def run_pass(tree):
        b = IndexSymbols()
        new_tree = b.transform(tree)

        return new_tree

    @singledispatchmethod
    def transform(self, arg):
        return arg

    @transform.register
    def _(self, arg: ASTSymbolTableRoot):
        self.initialize()
        self.symbols = arg.symbol_table
        for symbol in arg.symbol_table.values():
            if isinstance(symbol, FunctionSymbol):
                self.function_list.append(symbol)
                symbol.index = len(self.function_list) - 1
            elif isinstance(symbol, StructSymbol):
                self.struct_list.append(symbol)
                symbol.index = len(self.struct_list) - 1
            elif isinstance(symbol, ConstantSymbol):
                self.constant_list.append(symbol)

        for function in arg.functions:
            self.transform(function)

        return arg

    @transform.register
    def _(self, arg: ASTSymbolFunction):
        for statement in arg.statements:
            self.transform(statement)

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
