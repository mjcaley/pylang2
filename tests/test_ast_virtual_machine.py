import pytest

from pylang2.assembler.ast import *
from pylang2.assembler.passes.ast_pass import ASTPass
from pylang2.assembler.passes.phase2 import ASTVirtualMachine
from pylang2.assembler.parser import parser


def test_init():
    tree = parser.parse("""
    define test = 42
    """)
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)

    assert ast is vm.tree
    assert "test" in vm.definition_map


def test_integer():
    tree = parser.parse("""
    define test = 42
    """)
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run()

    assert Kind.Constant == result.symbol_table.get("test").kind
    assert Type.Int32 == result.symbol_table.get("test").type_
    assert 42 == result.symbol_table.get("test").value


def test_float():
    tree = parser.parse("""
    define test = 42.0 f32
    """)
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run()

    assert Kind.Constant == result.symbol_table.get("test").kind
    assert Type.Float32 == result.symbol_table.get("test").type_
    assert 42 == result.symbol_table.get("test").value


def test_string():
    tree = parser.parse("""
    define test = "test string"
    """)
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run()

    assert Kind.String == result.symbol_table.get("test").kind
    assert Type.String == result.symbol_table.get("test").type_
    assert 0 == result.symbol_table.get("test").value


def test_symbol():
    tree = parser.parse("""
    define test = reference
    define reference = 42
    """)
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run()

    assert Kind.Constant == result.symbol_table.get("test").kind
    assert Type.Int32 == result.symbol_table.get("test").type_
    assert 42 == result.symbol_table.get("test").value


def test_recursive():
    tree = parser.parse("""
        define test1 = test2
        define test2 = test1
        """)
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)

    with pytest.raises(RecursionError):
        vm.run()
