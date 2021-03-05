from dataclasses import dataclass, field
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


class Kind(Enum):
    Function = auto()
    Struct = auto()
    Label = auto()
    String = auto()
    Constant = auto()
    Binding = auto()


@dataclass
class Symbol:
    kind: Kind
    type_: Optional[Type] = None
    value: Any = None


class SymbolTable:
    def __init__(self):
        self._table = {}

    def declare(
        self, symbol, kind: Kind, type_: Optional[Type] = None, value: Any = None
    ):
        if self.is_declared(symbol):
            raise ValueError("Symbol already exists in scope")
        else:
            self._table[symbol] = Symbol(kind, type_, value)

    def update(
        self,
        symbol,
        kind: Kind = None,
        type_: Type = None,
        value: Any = None,
    ):
        symbol_value = self._table[symbol]
        if kind:
            symbol_value.kind = kind
        if type_:
            symbol_value.type_ = type_
        if value:
            symbol_value.value = value

    def get(self, symbol) -> Symbol:
        return self._table[symbol]

    def is_declared(self, symbol):
        return symbol in self._table


class ASTRoot(Tree):
    def __init__(self, children, symbol_table=None, string_pool=None, meta=None):
        self.symbol_table = symbol_table or SymbolTable()
        self.string_pool: list[str] = string_pool or []
        super().__init__("start", children, meta)


class ASTDefinition(Tree):
    def __init__(self, children, symbol, meta=None):
        self.symbol = symbol
        super().__init__("definition", children, meta)


class ASTFunction(Tree):
    def __init__(
        self,
        children,
        symbol: str,
        num_locals: int,
        num_args: int,
        name_index: Optional[int] = None,
        index: Optional[int] = None,
        address: Optional[int] = None,
        symbol_table: Optional[SymbolTable] = None,
        meta=None,
    ):
        self.symbol = symbol
        self.num_locals = num_locals
        self.num_args = num_args
        self.name_index = name_index
        self.index = index
        self.address = address
        self.symbol_table = symbol_table or SymbolTable()
        super().__init__("function", children, meta)


class ASTStruct(Tree):
    def __init__(
        self,
        children,
        symbol: str,
        struct_index: Optional[int] = None,
        meta=None,
        index=None,
    ):
        self.symbol = symbol
        self.struct_index = struct_index
        self.index = index
        super().__init__("struct", children, meta)


class ASTInstruction(Tree):
    def __init__(self, children, instruction: Instruction, type_: Type, meta=None):
        self.instruction = instruction
        self.type_ = type_
        super().__init__("instruction", children, meta)


class ASTLabel(Tree):
    def __init__(self, children, symbol: str, meta=None, address: int = None):
        self.symbol = symbol
        self.address = address
        super().__init__("label", children, meta)


class ASTOperand(Tree):
    def __init__(
        self, data, type_: Optional[Type] = None, value: Any = None, meta=None
    ):
        self.type_ = type_
        self.value = value
        super().__init__(data, [], meta)


class ASTInteger(ASTOperand):
    def __init__(self, type_: Optional[Type] = None, value: Any = None, meta=None):
        super().__init__("int_operand", type_, value, meta)


class ASTFloat(ASTOperand):
    def __init__(self, type_: Optional[Type] = None, value: Any = None, meta=None):
        super().__init__("float_operand", type_, value, meta)


class ASTString(ASTOperand):
    def __init__(self, value: int, string_value: str, meta=None):
        self.string_value = string_value
        super().__init__("str_operand", Type.String, value, meta)


class ASTSymbol(ASTOperand):
    def __init__(
        self, symbol, type_: Optional[Type] = None, value: Any = None, meta=None
    ):
        self.symbol = symbol
        super().__init__("binding", type_, value, meta)


class ASTLiteral(Tree):
    def __init__(self, value: Any, data: str, meta=None):
        self.value = value
        super().__init__(data, [], meta)


# Deprecated
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
        self,
        symbol: str,
        symbol_constant: Constant,
        data,
        children,
        meta=None,
        index=None,
    ):
        self.symbol = symbol
        self.index = index
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


class StringNode(Tree):
    def __init__(self, constant, index, data, children, meta=None):
        self.constant = constant
        self.index = index
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
        self.code = b""
        super().__init__(data, children, meta)
