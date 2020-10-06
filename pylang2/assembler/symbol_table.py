from dataclasses import dataclass
from enum import auto, Enum
from typing import Any
from lark import Visitor


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
class FunctionSymbol:
    address: int
    locals: int
    arguments: int


@dataclass
class ConstantSymbol:
    type_: Type
    value: Any


@dataclass
class StructSymbol:
    types: list[Type]


# TODO: probably don't need a dataclass for this
@dataclass
class SymbolTable:
    symbols: dict[str, Any]
