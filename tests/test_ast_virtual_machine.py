import pytest

from pylang2.assembler.ast import *
from pylang2.assembler.passes.ast_pass import ASTPass
from pylang2.assembler.passes.phase2 import ASTVirtualMachine
from pylang2.assembler.parser import parser


def test_init():
    tree = parser.parse(
        """
    define test = 42
    """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)

    assert ast is vm.tree
    assert "test" in vm._definition_map


def test_notimplemented():
    tree = parser.parse(
        """
    func test locals=0, args=0
        ret
    """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)

    with pytest.raises(NotImplementedError):
        vm.visit(None)


def test_integer():
    tree = parser.parse(
        """
    define test = 42
    """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run(ast.children[0])

    assert Kind.Constant == result.kind
    assert Type.Int32 == result.type_
    assert 42 == result.value


def test_float():
    tree = parser.parse(
        """
    define test = 42.0 f32
    """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run(ast.children[0])

    assert Kind.Constant == result.kind
    assert Type.Float32 == result.type_
    assert 42 == result.value


def test_string():
    tree = parser.parse(
        """
    define test = "test string"
    """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run(ast.children[0])

    assert Kind.String == result.kind
    assert Type.String == result.type_
    assert 0 == result.value


def test_symbol():
    tree = parser.parse(
        """
    define test = reference
    define reference = 42
    """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)
    result = vm.run(ast.children[0])

    assert Kind.Constant == result.kind
    assert Type.Int32 == result.type_
    assert 42 == result.value


def test_recursive():
    tree = parser.parse(
        """
        define test1 = test2
        define test2 = test1
        """
    )
    ast = ASTPass().transform(tree)
    vm = ASTVirtualMachine(ast)

    with pytest.raises(RecursionError):
        vm.run(ast.children[0])
