from dataclasses import dataclass, field
from enum import auto, Enum
from functools import singledispatchmethod
from pprint import pformat
from typing import Any, Optional, Union

from lark import Transformer, Discard, v_args

from .errors import Error, Redefinition


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


type_mapping = {
    "I8": Type.Int8,
    "I16": Type.Int16,
    "I32": Type.Int32,
    "I64": Type.Int64,
    "U8": Type.UInt8,
    "U16": Type.UInt16,
    "U32": Type.UInt32,
    "U64": Type.UInt64,
    "F32": Type.Float32,
    "F64": Type.Float64,
    "ADDR": Type.Address,
    "STR": Type.String
}


class Symbol:
    pass


@dataclass
class FunctionSymbol(Symbol):
    locals: int
    arguments: int
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
class DefinitionSymbol(Symbol):
    symbol: str


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
class ASTStatement:
    pass


@dataclass
class ASTNullaryInstruction(ASTStatement):
    instruction: Instruction


@dataclass
class ASTUnaryInstruction(ASTStatement):
    instruction: Instruction
    operand: Union[Constant, str]


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
    symbol_table: dict[str, Symbol] = field(default_factory=dict)
    constants: set[Constant] = field(default_factory=set)
    functions: list[ASTFunction] = field(default_factory=list)


@v_args(inline=True)
class ToAST(Transformer):
    def __init__(self, *args, **kwargs) -> None:
        self.errors: list[Error] = list()
        self.symbols: dict[str, Any] = dict()
        self.constants: set[Constant] = set()

        super().__init__(*args, **kwargs)

    @v_args(inline=False)
    def start(self, tree):
        return ASTRoot(self.errors, self.symbols, self.constants, tree)

    def definition(self, name_token, operand):
        symbol = name_token.value
        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, name_token.line, name_token.column))
        else:
            self.symbols[symbol] = operand

        raise Discard()

    def struct(self, name_token, types):
        symbol = name_token.value
        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, name_token.line, name_token.column))
        else:
            self.symbols[symbol] = StructSymbol(types)

        raise Discard()

    @v_args(inline=False)
    def types(self, tree):
        return [type_mapping[t.type] for t in tree]

    def function(self, name_token, locals_token, args_token, statements):
        symbol = name_token.value
        locals = int(locals_token.value)
        args = int(args_token.value)

        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, name_token.line, name_token.column))
        else:
            self.symbols[symbol] = FunctionSymbol(locals, args)
            return ASTFunction(symbol, statements)

    def statements(self, *stmts):
        return stmts

    def nullary_instruction(self, ins_token):
        instruction = instruction_mapping[ins_token.type]

        return ASTNullaryInstruction(instruction)

    def unary_instruction(self, ins_token, operand):
        instruction = instruction_mapping[ins_token.type]

        return ASTUnaryInstruction(instruction, operand)

    def label(self, token):
        symbol = token.value
        if symbol in self.symbols:
            self.errors.append(Redefinition(symbol, token.line, token.column))
        else:
            self.symbols[symbol] = LabelSymbol(symbol)

        return ASTLabel(symbol)

    def int_operand(self, value, type_token=None):
        type_def = "I32"
        if type_token:
            type_def = type_token.type

        constant = Constant(type_mapping[type_def], int(value.value))
        self.constants.add(constant)

        return constant

    def float_operand(self, value, type_token):
        type_def = type_mapping[type_token.type]

        constant = Constant(type_def, float(value.value))
        self.constants.add(constant)

        return constant

    def str_operand(self, value, _=None):
        constant = Constant(Type.String, value.value)
        self.constants.add(constant)

        return constant

    def binding(self, token):
        return token.value


class ASTPrinter:
    def __init__(self, indent="    "):
        self.indent = ""
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
