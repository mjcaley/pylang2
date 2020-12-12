from functools import singledispatchmethod
from pprint import pformat

from ..ast import (
    ASTRoot,
    ASTSymbolTableRoot,
    ASTDefinition,
    ASTStruct,
    ASTFunction,
    ASTSymbolFunction,
    ASTNullaryInstruction,
    ASTUnaryInstruction,
    ASTLabel,
    ASTOperand,
    Constant,
    Type,
)


class PrintAST:
    def __init__(self, indent="    "):
        self.indent = ""
        self.level = indent

    @staticmethod
    def run_pass(tree):
        print_ast = PrintAST()
        print_ast.visit(tree)

    def increment(self):
        self.indent += self.level

    def decrement(self):
        self.indent = self.indent[: len(self.level)]

    @singledispatchmethod
    def visit(self, args):
        raise NotImplementedError(f"visit method for type {args.__class__.__name__} not defined")

    @visit.register
    def _(self, arg: ASTRoot):
        print(f"{self.indent}{arg.__class__.__name__}")
        self.increment()
        for child in arg.children:
            self.visit(child)
        self.decrement()

    @visit.register
    def _(self, arg: ASTSymbolTableRoot):
        print(f"{self.indent}Symbols: {pformat(arg.symbol_table)}")
        print(f"{self.indent}Constants: {pformat(arg.constants)}")
        print(f"{self.indent}{arg.__class__.__name__}")
        self.increment()
        for function in arg.functions:
            self.visit(function)
        self.decrement()

    @visit.register
    def _(self, arg: ASTDefinition):
        print(f"{self.indent}{arg.__class__.__name__}(name={arg.name})")
        self.increment()
        self.visit(arg.operand)
        self.decrement()

    @visit.register
    def _(self, arg: ASTStruct):
        print(f"{self.indent}{arg.__class__.__name__}(name={arg.name}")
        self.increment()
        for t in arg.types:
            self.visit(t)

    @visit.register
    def _(self, arg: ASTFunction):
        print(
            f"{self.indent}{arg.__class__.__name__}(name={arg.name}, locals={arg.num_locals}, args={arg.num_args})"
        )
        self.increment()
        for statement in arg.statements:
            self.visit(statement)
        self.decrement()

    @visit.register
    def _(self, arg: ASTSymbolFunction):
        print(f"{self.indent}{arg.__class__.__name__}(name={arg.name})")
        self.increment()
        for statement in arg.statements:
            self.visit(statement)
        self.decrement()

    @visit.register
    def _(self, arg: ASTNullaryInstruction):
        print(f"{self.indent}{arg.__class__.__name__} {arg.instruction}")

    @visit.register
    def _(self, arg: ASTUnaryInstruction):
        print(f"{self.indent}{arg.__class__.__name__} {arg.instruction}")
        self.increment()
        self.visit(arg.operand)
        self.decrement()

    @visit.register
    def _(self, arg: ASTLabel):
        print(f"{self.indent}{arg.__class__.__name__}: {arg.name}")

    @visit.register
    def _(self, arg: ASTOperand):
        print(f"{self.indent}{arg.__class__.__name__}")
        self.increment()
        self.visit(arg.value)
        self.decrement()

    @visit.register
    def _(self, arg: Constant):
        print(f"{self.indent}Constant: {arg.type_}, {arg.value}")

    @visit.register
    def _(self, arg: str):
        print(f"{self.indent}Symbol: {arg}")

    @visit.register
    def _(self, type_: Type):
        print(f"{self.indent}{type_}")
