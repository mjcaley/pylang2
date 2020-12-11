from functools import singledispatchmethod

from ..ast import (
    Constant,
    Instruction,
    Type,
    ASTRoot,
    ASTDefinition,
    ASTStruct,
    ASTFunction,
    ASTLabel,
    ASTNullaryInstruction,
    ASTUnaryInstruction,
    ASTOperand,
    ASTSymbolTableRoot,
    Symbol,
    FunctionSymbol,
    StructSymbol,
    LabelSymbol,
)


class ToSymbolTableAST:
    def __init__(self):
        self.symbols: dict[str, Symbol] = dict()
        self.constants: set[Constant] = set()

    @staticmethod
    def run_pass(tree):
        pass

    @singledispatchmethod
    def transform(self, arg):
        return arg

    @transform.register
    def _(self, root: ASTRoot):
        functions: list[ASTFunction] = [
            self.transform(child) for child in root.children if child is not None
        ]

        return ASTSymbolTableRoot(self.symbols, self.constants, functions)

    @transform.register
    def _(self, definition: ASTDefinition):
        constant = definition.operand.value
        self.symbols[definition.name] = constant
