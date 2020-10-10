import pytest

from lark import Lark

from pylang2.assembler import parser
from pylang2.assembler.ast import ToAST


@pytest.fixture
def ast_parser():
    def inner(start_rule):
        return Lark(parser.grammar, parser="lalr", start=start_rule, transformer=ToAST())
    yield inner


def test_binding_returns_operand(ast_parser):
    result = ast_parser("binding").parse("test")

    assert "test" == result.symbol


def test_int_literal_with_type(ast_parser):
    result = ast_parser("int_operand").parse("42 i32")

    assert "lit_I32L1C1" == result.symbol


def test_int_literal_without_type(ast_parser):
    result = ast_parser("int_operand").parse("42")

    assert "lit_I32L1C1" == result.symbol
