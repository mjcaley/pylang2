from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Any, Optional
from lark import Visitor

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


@dataclass
class FunctionSymbol:
    locals: int
    arguments: int
    address: Optional[int] = None


@dataclass
class LabelSymbol:
    address: Optional[int]


@dataclass
class ConstantSymbol:
    type_: Optional[Type]
    value: Any


@dataclass
class StructSymbol:
    types: list[Type]


@dataclass
class SymbolTable:
    errors: list[Error] = field(default_factory=list)
    symbols: dict[str, Any] = field(default_factory=dict)


class SymbolTableGenerator(Visitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def struct(self, tree):
        name = tree.children[0]
        types = [type_mapping[t.type] for t in tree.children[1].children]
        if name.value not in self.symbol_table.symbols:
            self.symbol_table.symbols[name.value] = StructSymbol(types)
        else:
            self.symbol_table.errors.append(Redefinition(
                name.value,
                name.line,
                name.column
            ))

    def definition(self, tree):
        name = tree.children[0]
        if name not in self.symbol_table.symbols:
            self.symbol_table.symbols[name.value] = ConstantSymbol(None, tree[1])
        else:
            self.symbol_table.errors.append(Redefinition(
                name.value,
                name.line,
                name.column)
            )

    def label(self, tree):
        name = tree.children[0]
        if name not in self.symbol_table.symbols:
            self.symbol_table.symbols[name.value] = LabelSymbol()
        else:
            self.symbol_table.errors.append(Redefinition(
                name.value,
                name.line,
                name.column
            ))

    def function(self, tree):
        name = tree.children[0]
        num_locals = tree.children[1].value
        num_args = tree.children[2].value

        if name.value not in self.symbol_table.symbols:
            self.symbol_table.symbols[name.value] = FunctionSymbol(int(num_locals), int(num_args))
        else:
            self.symbol_table.errors.append(Redefinition(
                name.value,
                name.line,
                name.column)
            )
