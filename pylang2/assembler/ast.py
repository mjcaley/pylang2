from dataclasses import dataclass, field
from enum import auto, Enum
from functools import singledispatchmethod
from pprint import pformat
from typing import Any, Optional, Union


class Type(Enum):
    Int8 = auto()
    Int16 = auto()
    Int32 = auto()
    Int64 = auto()
    UInt8 = auto()
    UInt16 = auto()
    UInt32 = auto()
    UInt64 = auto()
    Float32 = auto()
    Float64 = auto()
    Address = auto()
    String = auto()


@dataclass
class Constant:
    type_: Optional[Type]
    value: Any

    def __hash__(self):
        return hash((self.__class__, self.type_, self.value))


class Instruction(Enum):
    Halt = auto()
    Noop = auto()
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()
    Mod = auto()
    LdConst = auto()
    LdLocal = auto()
    StLocal = auto()
    Pop = auto()
    TestEQ = auto()
    TestNE = auto()
    TestLT = auto()
    TestGT = auto()
    Jmp = auto()
    JmpT = auto()
    JmpF = auto()
    CallFunc = auto()
    CallVirt = auto()
    Ret = auto()
    NewStruct = auto()
    LdField = auto()
    StField = auto()
    NewArray = auto()
    LdElem = auto()
    StElem = auto()


@dataclass
class ASTOperand:
    value: Constant
    line: int
    column: int


@dataclass
class ASTDefinition:
    name: str
    operand: ASTOperand
    line: int
    column: int


@dataclass
class ASTStruct:
    name: str
    types: list[Type]
    line: int
    column: int


class ASTStatement:
    pass


@dataclass
class ASTNullaryInstruction(ASTStatement):
    instruction: Instruction
    line: int
    column: int


@dataclass
class ASTUnaryInstruction(ASTStatement):
    instruction: Instruction
    operand: Union[Constant, str]
    line: int
    column: int


@dataclass
class ASTLabel(ASTStatement):
    name: str
    line: int
    column: int


@dataclass
class ASTFunction:
    name: str
    num_locals: int
    num_args: int
    statements: list[ASTStatement]
    line: int
    column: int


@dataclass
class ASTRoot:
    children: list[Union[ASTDefinition, ASTStruct, ASTFunction]]


# Symbol AST


class Symbol:
    pass


@dataclass
class FunctionSymbol(Symbol):
    name: Constant
    num_locals: int
    num_args: int
    address: Optional[int] = None


@dataclass
class LabelSymbol(Symbol):
    address: Optional[int] = None


@dataclass
class StructSymbol(Symbol):
    types: list[Type]

    def __hash__(self):
        return hash(self.types)


@dataclass
class ConstantSymbol(Symbol):
    constant: Constant


@dataclass
class ASTSymbolFunction:
    name: str
    statements: list[ASTStatement]


@dataclass
class ASTSymbolTableRoot:
    symbol_table: dict[str, Symbol] = field(default_factory=dict)
    constants: set[Constant] = field(default_factory=set)
    functions: list[ASTFunction] = field(default_factory=list)


# @v_args(inline=True)
# class ToAST(Transformer):
#     def __init__(self, *args, **kwargs) -> None:
#         self.symbols: dict[str, Any] = dict()
#         self.constants: set[Constant] = set()
#
#         super().__init__(*args, **kwargs)
#
#     @v_args(inline=False)
#     def start(self, tree):
#         return ASTRoot(self.symbols, self.constants, tree)
#
#     def definition(self, name_token, operand):
#         symbol = name_token.value
#         self.symbols[symbol] = operand
#
#         raise Discard()
#
#     def struct(self, name_token, types):
#         symbol = name_token.value
#         self.symbols[symbol] = StructSymbol(types)
#
#         raise Discard()
#
#     @v_args(inline=False)
#     def types(self, tree):
#         return [type_mapping[t.type] for t in tree]
#
#     def function(self, name_token, locals_token, args_token, statements):
#         symbol = name_token.value
#         locals = int(locals_token.value)
#         args = int(args_token.value)
#
#         self.symbols[symbol] = FunctionSymbol(locals, args)
#         return ASTFunction(symbol, statements)
#
#     def statements(self, *stmts):
#         return stmts
#
#     def nullary_instruction(self, ins_token):
#         instruction = instruction_mapping[ins_token.type]
#
#         return ASTNullaryInstruction(instruction)
#
#     def unary_instruction(self, ins_token, operand):
#         instruction = instruction_mapping[ins_token.type]
#
#         return ASTUnaryInstruction(instruction, operand)
#
#     def label(self, token):
#         symbol = token.value
#         self.symbols[symbol] = LabelSymbol(symbol)
#
#         return ASTLabel(symbol)
#
#     def int_operand(self, value, type_token=None):
#         type_def = "I32"
#         if type_token:
#             type_def = type_token.type
#
#         constant = Constant(type_mapping[type_def], int(value.value))
#         self.constants.add(constant)
#
#         return constant
#
#     def float_operand(self, value, type_token):
#         type_def = type_mapping[type_token.type]
#
#         constant = Constant(type_def, float(value.value))
#         self.constants.add(constant)
#
#         return constant
#
#     def str_operand(self, value, _=None):
#         constant = Constant(Type.String, value.value)
#         self.constants.add(constant)
#
#         return constant
#
#     def binding(self, token):
#         return token.value


class ASTPrinter:
    def __init__(self, indent="    "):
        self.indent = ""
        self.level = indent

    def increment(self):
        self.indent += self.level

    def decrement(self):
        self.indent = self.indent[: len(self.level)]

    @singledispatchmethod
    def visit(self, args):
        raise NotImplementedError

    @visit.register
    def _(self, arg: ASTRoot):
        print(f"{self.indent}Symbols: {pformat(arg.symbol_table)}")
        print(f"{self.indent}Constants: {pformat(arg.constants)}")
        print(f"{self.indent}ASTRoot")
        self.increment()
        for function in arg.functions:
            self.visit(function)
        self.decrement()

    @visit.register
    def _(self, arg: ASTFunction):
        print(f"{self.indent}ASTFunction(name={arg.symbol})")
        self.increment()
        for statement in arg.statements:
            self.visit(statement)
        self.decrement()

    @visit.register
    def _(self, arg: ASTNullaryInstruction):
        print(f"{self.indent}ASTNullaryInstruction {arg.instruction}")

    @visit.register
    def _(self, arg: ASTUnaryInstruction):
        print(f"{self.indent}ASTUnaryInstruction {arg.instruction}")
        self.increment()
        self.visit(arg.operand)
        self.decrement()

    @visit.register
    def _(self, arg: ASTLabel):
        print(f"{self.indent}ASTLabel: {arg.symbol}")

    @visit.register
    def _(self, arg: Constant):
        print(f"{self.indent}Constant: {arg.type_}, {arg.value}")

    @visit.register
    def _(self, arg: str):
        print(f"{self.indent}Symbol: {arg}")
