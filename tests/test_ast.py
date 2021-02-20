import pytest

from pylang2.assembler.ast import SymbolTable, Symbol, Kind, Type


def test_is_declared_false():
    symbol_table = SymbolTable()

    assert False is symbol_table.is_declared("test")


def test_is_declared_true():
    symbol_table = SymbolTable()
    symbol_table.declare("test", Kind.Function, Type.UInt64)

    assert True is symbol_table.is_declared("test")


def test_declare_and_get():
    symbol_table = SymbolTable()
    symbol_table.declare("test", Kind.String, Type.String, "value")
    result = symbol_table.get("test")

    assert isinstance(result, Symbol)
    assert Kind.String == result.kind
    assert Type.String == result.type_
    assert "value" == result.value


def test_declare_exists():
    symbol_table = SymbolTable()
    symbol_table.declare("test", Kind.String, Type.String, "value")

    with pytest.raises(ValueError):
        symbol_table.declare("test", Kind.String, Type.String, "value")


def test_update():
    symbol_table = SymbolTable()
    symbol_table.declare("test", Kind.String, Type.String, "value")
    symbol_table.update("test", Kind.Constant, Type.Int32, 42)
    result = symbol_table.get("test")

    assert Kind.Constant == result.kind
    assert Type.Int32 == result.type_
    assert 42 == result.value
