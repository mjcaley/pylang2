from dataclasses import dataclass, field
from enum import auto, Enum
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
    value: Union[Constant, str]
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
    operand: ASTOperand
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
    functions: list[ASTSymbolFunction] = field(default_factory=list)
