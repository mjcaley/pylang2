import pytest

from lark import Lark

from pylang2.assembler import parser
from pylang2.assembler.ast import ToAST, Type


@pytest.fixture
def ast_parser():
    def inner(start_rule):
        return Lark(parser.grammar, parser="lalr", start=start_rule)
    yield inner


def test_binding_returns_operand(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("binding").parse("test"))

    assert "test" == result.symbol


def test_int_literal_with_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("int_operand").parse("42 i32"))

    assert "lit_I32L1C1" == result.symbol
    assert 42 == to_ast.symbols["lit_I32L1C1"].value
    assert Type.Int32 == to_ast.symbols["lit_I32L1C1"].type_


def test_int_literal_without_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("int_operand").parse("42"))

    assert "lit_I32L1C1" == result.symbol
