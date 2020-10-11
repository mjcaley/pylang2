from dataclasses import dataclass, field
from enum import auto, Enum
from functools import singledispatchmethod
from pprint import pprint
from typing import Any

from lark import Transformer, Discard, v_args

from .errors import Error, Redefinition
from .symbol_table import Type, type_mapping, FunctionSymbol, LabelSymbol, ConstantSymbol, StructSymbol


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


instruction_mapping = {
    "HALT": Instruction.Halt,
    "NOOP": Instruction.Noop,
    "ADD": Instruction.Add,
    "SUB": Instruction.Sub,
    "MUL": Instruction.Mul,
    "DIV": Instruction.Div,
    "MOD": Instruction.Mod,
    "LDCONST": Instruction.LdConst,
    "LDLOCAL": Instruction.LdLocal,
    "STLOCAL": Instruction.StLocal,
    "POP": Instruction.Pop,
    "TESTEQ": Instruction.TestEQ,
    "TESTNE": Instruction.TestNE,
    "TESTLT": Instruction.TestLT,
    "TESTGT": Instruction.TestGT,
    "JMP": Instruction.Jmp,
    "JMPT": Instruction.JmpT,
    "JMPF": Instruction.JmpF,
    "CALLFUNC": Instruction.CallFunc,
    "CALLVIRT": Instruction.CallVirt,
    "RET": Instruction.Ret,
    "NEWSTRUCT": Instruction.NewStruct,
    "LDFIELD": Instruction.LdField,
    "STFIELD": Instruction.StField,
    "NEWARRAY": Instruction.NewArray,
    "LDELEM": Instruction.LdElem,
    "STELEM": Instruction.StElem,
}


@dataclass
class ASTOperand:
    symbol: str


@dataclass
class ASTStatement:
    pass


@dataclass
class ASTNullaryInstruction(ASTStatement):
    instruction: Instruction


@dataclass
class ASTUnaryInstruction(ASTStatement):
    instruction: Instruction
    operand: ASTOperand


@dataclass
class ASTLabel(ASTStatement):
    symbol: str


@dataclass
class ASTFunction:
    symbol: str
    statements: list[ASTStatement]


@dataclass
class ASTRoot:
    errors: list[Error] = field(default_factory=list)
    symbols: dict[str, Any] = field(default_factory=dict)
    functions: list[ASTFunction] = field(default_factory=list)


class ToAST(Transformer):
    def __init__(self, *args, **kwargs) -> None:
        self.errors: list[Error] = list()
        self.symbols: dict[str, Any] = dict()

        super().__init__(*args, **kwargs)

    @staticmethod
    def literal_name(type: str, line: int, column: int) -> str:
        return f"lit_{type}L{line}C{column}"

    @staticmethod
    def label_name(name: str) -> str:
        return f"lbl_{name}"

    def start(self, tree):
        return ASTRoot(self.errors, self.symbols, tree)

    @v_args(inline=True)
    def definition(self, name_token, operand):
        symbol = name_token.value
        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, name_token.line, name_token.column))
        else:
            self.symbols[symbol] = self.symbols[operand.symbol]

        raise Discard()

    @v_args(inline=True)
    def struct(self, name_token, types):
        symbol = name_token.value
        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, name_token.line, name_token.column))
        else:
            self.symbols[symbol] = StructSymbol(types)

        raise Discard()

    def types(self, tree):
        return [type_mapping[t.type] for t in tree]

    @v_args(inline=True)
    def function(self, name_token, locals_token, args_token, statements):
        symbol = name_token.value
        locals = int(locals_token.value)
        args = int(args_token.value)

        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, name_token.line, name_token.column))
        else:
            self.symbols[symbol] = FunctionSymbol(locals, args, None)
            return ASTFunction(symbol, statements)

    @v_args(inline=True)
    def statements(self, *stmts):
        return stmts

    @v_args(inline=True)
    def nullary_instruction(self, ins_token):
        instruction = instruction_mapping[ins_token.type]

        return ASTNullaryInstruction(instruction)

    @v_args(inline=True)
    def unary_instruction(self, ins_token, operand):
        instruction = instruction_mapping[ins_token.type]

        return ASTUnaryInstruction(instruction, operand)

    @v_args(inline=True)
    def label(self, token):
        symbol = self.label_name(token.value)
        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, token.line, token.column))
        else:
            self.symbols[symbol] = LabelSymbol(None)

        return ASTLabel(symbol)

    @v_args(inline=True)
    def int_operand(self, value, type_token=None):
        type_def = "I32"
        if type_token:
            type_def = type_token.type
        symbol_name = self.literal_name(type_def, value.line, value.column)

        self.symbols[symbol_name] = ConstantSymbol(type_mapping[type_def], int(value.value))

        return ASTOperand(symbol_name)

    @v_args(inline=True)
    def float_operand(self, value, type_token):
        type_def = type_mapping[type_token.type]
        symbol_name = self.literal_name(type_def, value.line, value.column)

        self.symbols[symbol_name] = ConstantSymbol(type_def, float(value.value))

        return ASTOperand(symbol_name)

    @v_args(inline=True)
    def str_operand(self, value, _=None):
        symbol_name = self.literal_name("str", value.line, value.column)

        self.symbols[symbol_name] = ConstantSymbol(Type.String, value.value)

        return ASTOperand(symbol_name)

    @v_args(inline=True)
    def binding(self, token):
        return ASTOperand(token.value)


class ASTPrinter:
    def __init__(self, indent="    "):
        self.indent = indent
        self.level = indent

    def increment(self):
        self.indent += self.level

    def decrement(self):
        self.indent = self.indent[:len(self.level)]

    @singledispatchmethod
    def visit(self, args):
        raise NotImplementedError

    @visit.register
    def _(self, arg: ASTRoot):
        print(f"Symbols: {pprint(arg.symbols)}")
        print(f"ASTRoot")
        self.increment()
        for function in arg.functions:
            self.visit(function)
        self.decrement()

    @visit.register
    def _(self, arg: ASTFunction):
        print(f"ASTFunction(name={arg.symbol}")
        self.increment()
        for statement in arg.statements:
            self.visit(statement)
        self.decrement()

    @visit.register
    def _(self, arg: ASTNullaryInstruction):
        print(f"ASTNullaryInstruction {arg.instruction}")

    @visit.register
    def _(self, arg: ASTUnaryInstruction):
        print(f"ASTUnaryInstruction {arg.instruction}")
        self.increment()
        self.visit(arg.operand)
        self.decrement()

    @visit.register
    def _(self, arg: ASTLabel):
        print(f"ASTLabel: {arg.symbol}")

    @visit.register
    def _(self, arg: ASTOperand):
        print(f"ASTOperand: {arg.symbol}")
