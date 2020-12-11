import pytest

from lark import Lark

from pylang2.assembler import parser
from pylang2.assembler.ast import (
    Type,
    ASTRoot,
    ASTDefinition,
    ASTStruct,
    ASTFunction,
    ASTLabel,
    ASTStatement,
    ASTOperand,
    Instruction,
)
from pylang2.assembler.passes.to_ast import ToAST


@pytest.fixture
def ast_parser():
    def inner(start_rule):
        return Lark(parser.grammar, parser="lalr", start=start_rule)

    yield inner


def test_start(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("start").parse(""))

    assert isinstance(result, ASTRoot)


def test_definition(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(
        ast_parser("definition").parse(
        """
        define name = 42 i32
        """
            )
        )

    assert isinstance(result, ASTDefinition)
    assert "name" == result.name
    assert isinstance(result.operand, ASTOperand)


def test_struct(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(
        ast_parser("struct").parse(
            """
        struct name
            i32
        """
        )
    )

    assert isinstance(result, ASTStruct)
    assert "name" == result.name
    assert None is not result.types


def test_types(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(
        ast_parser("types").parse(
            """
    i32
    i64
    str
    """
        )
    )

    assert Type.Int32 == result[0]
    assert Type.Int64 == result[1]
    assert Type.String == result[2]


def test_func(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(
        ast_parser("function").parse(
            """
    func name locals=1, args=2
        ret
    """
        )
    )

    assert isinstance(result, ASTFunction)
    assert "name" == result.name
    assert 1 == result.num_locals
    assert 2 == result.num_args
    assert None is not result.statements


def test_statements(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(
        ast_parser("statements").parse(
            """
        ldconst 42
        ret
    """
        )
    )

    assert all([isinstance(statement, ASTStatement) for statement in result])


def test_nullary_instruction(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("nullary_instruction").parse("ret"))

    assert Instruction.Ret == result.instruction


def test_unary_instruction(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("unary_instruction").parse("ldconst 42"))

    assert Instruction.LdConst == result.instruction
    assert isinstance(result.operand, ASTOperand)


def test_label(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("label").parse("label:"))

    assert isinstance(result, ASTLabel)
    assert "label" == result.name


def test_int_literal_with_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("int_operand").parse("42 i32"))

    assert isinstance(result, ASTOperand)
    assert 42 == result.value.value
    assert Type.Int32 == result.value.type_


def test_int_literal_without_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("int_operand").parse("42"))

    assert isinstance(result, ASTOperand)
    assert 42 == result.value.value
    assert Type.Int32 == result.value.type_


def test_float32_literal(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("float_operand").parse("4.2 f32"))

    assert isinstance(result, ASTOperand)
    assert 4.2 == result.value.value
    assert Type.Float32 == result.value.type_


def test_float64_literal(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("float_operand").parse("4.2 f64"))

    assert isinstance(result, ASTOperand)
    assert 4.2 == result.value.value
    assert Type.Float64 == result.value.type_


def test_string_literal(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("str_operand").parse('"this is a string"'))

    assert isinstance(result, ASTOperand)
    assert '"this is a string"' == result.value.value
    assert Type.String == result.value.type_


def test_string_literal_with_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("str_operand").parse('"this is a string" str'))

    assert isinstance(result, ASTOperand)
    assert '"this is a string"' == result.value.value
    assert Type.String == result.value.type_


def test_binding_returns_operand(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("binding").parse("test"))

    assert isinstance(result, ASTOperand)
    assert "test" == result.value
