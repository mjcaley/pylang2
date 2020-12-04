import pytest

from lark import Lark, Discard

from pylang2.assembler import parser
from pylang2.assembler.ast import StructSymbol, ToAST, Type, ASTRoot, ASTFunction, ASTLabel, ASTStatement, Constant, Instruction
from pylang2.assembler.errors import Redefinition


@pytest.fixture
def ast_parser():
    def inner(start_rule):
        return Lark(parser.grammar, parser="lalr", start=start_rule)
    yield inner


def test_start(ast_parser, mocker):
    to_ast = ToAST()
    to_ast.symbols = mocker.stub()
    to_ast.errors = mocker.stub()
    to_ast.constants = mocker.stub()
    result = to_ast.transform(ast_parser("start").parse(""))

    assert isinstance(result, ASTRoot)
    assert to_ast.symbols is result.symbol_table
    assert to_ast.constants is result.constants
    assert to_ast.errors is result.errors


def test_definition(ast_parser):
    to_ast = ToAST()
    with pytest.raises(Discard):
        to_ast.transform(ast_parser("definition").parse("""
        define name = 42 i32
        """))

    assert "name" in to_ast.symbols
    assert to_ast.symbols["name"] in to_ast.constants
    assert isinstance(to_ast.symbols["name"], Constant)


def test_definition_redefined(ast_parser, mocker):
    to_ast = ToAST()
    to_ast.symbols["name"] = mocker.stub()
    with pytest.raises(Discard):
        to_ast.transform(ast_parser("definition").parse("""
        define name = 42 i32
        """))

    assert isinstance(to_ast.errors[0], Redefinition)


def test_struct(ast_parser):
    to_ast = ToAST()
    with pytest.raises(Discard):
        to_ast.transform(ast_parser("struct").parse("""
        struct name
            i32
        """))

    assert "name" in to_ast.symbols
    assert isinstance(to_ast.symbols["name"], StructSymbol)


def test_struct_redefined(ast_parser, mocker):
    to_ast = ToAST()
    to_ast.symbols["name"] = mocker.stub()
    with pytest.raises(Discard):
        to_ast.transform(ast_parser("struct").parse("""
        struct name
            i32
        """))

    assert isinstance(to_ast.errors[0], Redefinition)


def test_types(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("types").parse("""
    i32
    i64
    str
    """))

    assert Type.Int32 == result[0]
    assert Type.Int64 == result[1]
    assert Type.String == result[2]


def test_func(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("function").parse("""
    func name locals=1, args=2
        ret
    """))

    assert "name" in to_ast.symbols
    assert 1 == to_ast.symbols["name"].locals
    assert 2 == to_ast.symbols["name"].arguments
    assert isinstance(result, ASTFunction)
    assert "name" == result.symbol


def test_func_redefined(ast_parser, mocker):
    to_ast = ToAST()
    to_ast.symbols["name"] = mocker.stub()
    result = to_ast.transform(ast_parser("function").parse("""
    func name locals=1, args=2
        ret
    """))

    assert isinstance(to_ast.errors[0], Redefinition)


def test_statements(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("statements").parse("""
        ldconst 42
        ret
    """))

    assert all([isinstance(statement, ASTStatement) for statement in result])


def test_nullary_instruction(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("nullary_instruction").parse("ret"))

    assert Instruction.Ret == result.instruction


def test_unary_instruction(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("unary_instruction").parse("ldconst 42"))

    assert Instruction.LdConst == result.instruction
    assert isinstance(result.operand, Constant)


def test_label(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("label").parse("label:"))

    assert ASTLabel("label") == result
    assert "label" in to_ast.symbols


def test_label_throws_redefined(ast_parser, mocker):
    to_ast = ToAST()
    to_ast.symbols["label"] = mocker.stub()
    result = to_ast.transform(ast_parser("label").parse("label:"))

    assert isinstance(to_ast.errors[0], Redefinition)


def test_int_literal_with_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("int_operand").parse("42 i32"))

    assert result in to_ast.constants
    assert 42 == result.value
    assert Type.Int32 == result.type_


def test_int_literal_without_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("int_operand").parse("42"))

    assert result in to_ast.constants
    assert 42 == result.value
    assert Type.Int32 == result.type_


def test_float32_literal(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("float_operand").parse("4.2 f32"))

    assert result in to_ast.constants
    assert 4.2 == result.value
    assert Type.Float32 == result.type_


def test_float64_literal(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("float_operand").parse("4.2 f64"))

    assert result in to_ast.constants
    assert 4.2 == result.value
    assert Type.Float64 == result.type_


def test_string_literal(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("str_operand").parse('"this is a string"'))

    assert result in to_ast.constants
    assert '"this is a string"' == result.value
    assert Type.String == result.type_


def test_string_literal_with_type(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("str_operand").parse('"this is a string" str'))

    assert result in to_ast.constants
    assert '"this is a string"' == result.value
    assert Type.String == result.type_


def test_binding_returns_operand(ast_parser):
    to_ast = ToAST()
    result = to_ast.transform(ast_parser("binding").parse("test"))

    assert "test" == result
