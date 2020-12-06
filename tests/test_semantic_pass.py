import pytest

from pylang2.assembler.parser import parser
from pylang2.assembler.semantic_pass import CheckRedefinitions
from pylang2.assembler.errors import Redefinition


def test_redefinition_in_definition():
    tree = parser.parse("""
    define forty_two = 42
    define forty_two = 42
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_in_struct():
    tree = parser.parse("""
    struct test
        i32
    struct test
        u64
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_in_function():
    tree = parser.parse("""
    func test locals=1, args=1
        ret
    func test locals=2, args=2
        ret
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_in_label():
    tree = parser.parse("""
    func test locals=1, args=1
        test:
        ret
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_can_be_collected():
    tree = parser.parse("""
    func test locals=1, args=1
        test:
        ret
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)
