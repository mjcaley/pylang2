from dataclasses import dataclass
from enum import auto, Enum, IntEnum, unique
from typing import Any, NamedTuple, Optional

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
    Definition = auto()
    String = auto()
    Constant = auto()


@dataclass
class Symbol:
    kind: Kind
    type_: Type
    value: Any
    scope: Optional[dict[str, "Symbol"]]


class SymbolTable:
    def __init__(self):
        self._table = {}
        self._scope = []

    def _current_scope(self):
        scope = self._table
        for key in self._scope:
            scope = scope[key].scope

        return scope

    def declare(self, symbol, kind: Kind, type_: Type, value: Any = None):
        if self.is_declared(symbol):
            raise ValueError("Symbol already exists in scope")
        else:
            self._current_scope()[symbol] = Symbol(kind, type_, value, {})

    def update(self, symbol, kind: Kind, type_: Type, value: Any = None):
        symbol_value = self._current_scope()[symbol]
        symbol_value.kind = kind
        symbol_value.type_ = type_
        symbol_value.value = value

    def get(self, symbol):
        return self._current_scope()[symbol]

    def is_declared(self, symbol):
        scope = self._current_scope()

        return symbol in scope

    def push_scope(self, symbol):
        if self.is_declared(symbol):
            self._scope.append(symbol)
        else:
            raise ValueError("Symbol does not exist")

    def pop_scope(self):
        try:
            self._scope.pop()
        except IndexError as e:
            raise ValueError("Cannot pop from global scope") from e


class ASTRoot(Tree):
    def __init__(self, children, meta=None):
        self.symbol_table = SymbolTable()
        self.string_pool: set[str] = set()
        super().__init__("start", children, meta)


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
        meta=None,
    ):
        self.symbol = symbol
        self.num_locals = num_locals
        self.num_args = num_args
        self.name_index = name_index
        self.index = index
        self.address = address
        super().__init__("function", children, meta)


class ASTStruct(Tree):
    def __init__(
        self, children, symbol: str, struct_index: Optional[int] = None, meta=None, index=None
    ):
        self.symbol = symbol
        self.struct_index = struct_index
        self.index = index
        super().__init__("struct", children, meta)


class ASTInstruction(Tree):
    def __init__(self, data, children, instruction: Instruction, meta=None):
        self.instruction = instruction
        super().__init__(data, children, meta)


class ASTLabel(Tree):
    def __init__(self, children, symbol: str, meta=None, address: int = None):
        self.symbol = symbol
        self.address = address
        super().__init__("label", children, meta)


class ASTConstant(Tree):
    def __init__(self, data, value, type_: Optional[Type] = None, meta=None):
        self.value = value
        self.type_ = type_
        super().__init__(data, [], meta)


class ASTString(Tree):
    def __init__(self, value, index: Optional[int] = None, meta=None):
        self.value = value
        self.index = index
        super().__init__("str_operand", [], meta)


class ASTSymbol(Tree):
    def __init__(self, symbol, meta=None):
        self.symbol = symbol
        super().__init__("binding", [], meta)


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
        self, symbol: str, symbol_constant: Constant, data, children, meta=None, index=None
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
        self.code = b''
        super().__init__(data, children, meta)
