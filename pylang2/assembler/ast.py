from dataclasses import dataclass
from enum import auto, Enum, IntEnum, unique
from typing import Any, Optional

from lark import Tree


@unique
class Instruction(Enum):
    Halt = "halt"
    Noop = "noop"
    Add = "add"
    Sub = "sub"
    Mul = "mul"
    Div = "div"
    Mod = "mod"
    LdConst = "ldconst"
    LdLocal = "ldlocal"
    StLocal = "stlocal"
    Pop = "pop"
    TestEQ = "testeq"
    TestNE = "testne"
    TestLT = "testlt"
    TestGT = "testgt"
    Jmp = "jmp"
    JmpT = "jmpt"
    JmpF = "jmpf"
    CallFunc = "callfunc"
    CallVirt = "callvirt"
    Ret = "ret"
    NewStruct = "newstruct"
    LdField = "ldfield"
    StField = "stfield"
    NewArray = "newarray"
    LdElem = "ldelem"
    StElem = "stelem"


@unique
class Type(Enum):
    Void = None
    Int8 = "i8"
    Int16 = "i16"
    Int32 = "i32"
    Int64 = "i64"
    UInt8 = "u8"
    UInt16 = "u16"
    UInt32 = "u32"
    UInt64 = "u64"
    Float32 = "f32"
    Float64 = "f64"
    Address = "addr"
    String = "str"


@dataclass
class Constant:
    type_: Optional[Type]
    value: Any

    def __hash__(self):
        return hash((self.__class__, self.type_, self.value))


class SymbolKind(Enum):
    Unknown = auto()
    Struct = auto()
    Function = auto()
    Constant = auto()
    Label = auto()


class ErrorNode(Tree):
    def __init__(self, message, children, meta=None):
        self.message = message
        super().__init__("error", children, meta)


@dataclass
class SymbolTableValue:
    kind: SymbolKind
    type_: Optional[Type]


class SymbolTableNode(Tree):
    def __init__(self, data, children, meta=None, symbol_table=None, constants=None):
        self.symbol_table: dict[str, SymbolTableValue] = symbol_table or {}
        self.constants: set[Constant] = constants or set()
        super().__init__(data, children, meta)


class SymbolNode(Tree):
    def __init__(self, symbol: str, data, children, meta=None):
        self.symbol = symbol
        super().__init__(data, children, meta)


class StructNode(Tree):
    def __init__(
        self, symbol: str, symbol_constant: Constant, data, children, meta=None
    ):
        self.symbol = symbol
        self.symbol_constant = symbol_constant
        super().__init__(data, children, meta)


class FunctionNode(Tree):
    def __init__(
        self,
        symbol: str,
        constant: Constant,
        num_locals: int,
        num_args: int,
        data,
        children,
        meta=None,
        address: int = None,
        index: int = None,
    ):
        self.symbol = symbol
        self.symbol_constant = constant
        self.num_locals = num_locals
        self.num_args = num_args
        self.address = address
        self.index = index
        super().__init__(data, children, meta)


class InstructionNode(Tree):
    def __init__(self, instruction: Instruction, data, children, meta=None):
        self.instruction = instruction
        super().__init__(data, children, meta)


class LabelNode(Tree):
    def __init__(self, symbol: str, data, children, meta=None, address: int = None):
        self.symbol = symbol
        self.address = address
        super().__init__(data, children, meta)


class ConstantNode(Tree):
    def __init__(self, constant, data, children, meta=None):
        self.constant = constant
        super().__init__(data, children, meta)


# Code generation objects

class Bytecode(IntEnum):
    Halt = auto()
    Noop = auto()
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()
    Mod = auto()
    LdConstI8 = auto()
    LdConstI16 = auto()
    LdConstI32 = auto()
    LdConstI64 = auto()
    LdConstU8 = auto()
    LdConstU16 = auto()
    LdConstU32 = auto()
    LdConstU64 = auto()
    LdConstF32 = auto()
    LdConstF64 = auto()
    LdConstStr = auto()
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


class CodeGenRootNode(Tree):
    def __init__(self, data, children, meta=None):
        self.function_pool = []
        self.string_pool = []
        self.code = b''
        super().__init__(data, children, meta)
