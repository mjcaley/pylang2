import pytest

from lark import Lark

from pylang2.assembler.parser import grammar
from pylang2.assembler.passes.ast_pass import ASTPass
from pylang2.assembler.ast import *


@pytest.fixture
def parser():
    def inner(start_rule):
        return Lark(grammar, parser="lalr", start=start_rule)

    return inner


def test_start_rule(parser):
    tree = parser("start").parse("""
    define test1 = 42
    func test2 locals=1, args=2
        ret
    """)
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTRoot)
    assert ast_pass.symbol_table == ast.symbol_table
    assert ast_pass.string_pool == ast.string_pool


def test_definition_rule(parser):
    tree = parser("definition").parse("define test = 42")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTDefinition)
    assert "test" == ast.symbol


def test_struct_rule(parser):
    tree = parser("struct").parse(
        """
    struct test
        u8
    """
    )
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTStruct)
    assert "test" == ast.symbol
    assert all(isinstance(t, Type) for t in ast.children)
    assert Kind.Struct == ast_pass.symbol_table.get("test").kind
    assert Type.UInt64 == ast_pass.symbol_table.get("test").type_
    assert 0 == ast_pass.symbol_table.get("test").value


def test_struct_declared(parser):
    tree = parser("struct").parse(
        """
    struct test
        u8
    """
    )
    ast_pass = ASTPass()
    ast_pass.symbol_table.declare("test", Kind.Function, type_=Type.UInt64)
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ErrorNode)


def test_types_rule(parser):
    tree = parser("types").parse("i32 u8 str")
    ast = ASTPass().transform(tree)

    assert all(isinstance(t, Type) for t in ast)


def test_function_rule(parser):
    tree = parser("function").parse(
        """
    func test locals=1, args=2
        ret
    """
    )
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTFunction)
    assert "test" == ast.symbol
    assert 1 == ast.num_locals
    assert 2 == ast.num_args
    assert Kind.Function == ast_pass.symbol_table.get("test").kind
    assert Type.UInt64 == ast_pass.symbol_table.get("test").type_
    assert 0 == ast_pass.symbol_table.get("test").value
    assert None is not ast_pass.symbol_table.get("test").scope


def test_function_declared(parser):
    tree = parser("function").parse(
        """
    func test locals=1, args=2
        ret
    """
    )
    ast_pass = ASTPass()
    ast_pass.symbol_table.declare("test", Kind.Function, type_=Type.UInt64)
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ErrorNode)


def test_nullary_instruction_rule(parser):
    tree = parser("nullary_instruction").parse("ret")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTInstruction)
    assert Instruction.Ret == ast.instruction


def test_unary_instruction_rule(parser):
    tree = parser("unary_instruction").parse("ldconst 42")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTInstruction)
    assert Instruction.LdConst == ast.instruction
    assert isinstance(ast.children[0], ASTConstant)


def test_label_rule(parser):
    tree = parser("label").parse("test:")
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTLabel)
    assert "test" == ast.symbol
    assert Kind.Label == ast_pass.function_scope.get("test").kind
    assert Type.UInt64 == ast_pass.function_scope.get("test").type_


def test_label_declared(parser):
    tree = parser("label").parse("test:")
    ast_pass = ASTPass()
    ast_pass.function_scope.declare(symbol="test", kind=Kind.Label, type_=Type.UInt64)
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ErrorNode)


@pytest.mark.parametrize(
    "test_input,expected_type",
    [
        ("42", Type.Int32),
        ("42 i8", Type.Int8),
        ("42 i16", Type.Int16),
        ("42 i32", Type.Int32),
        ("42 i64", Type.Int64),
        ("42 u8", Type.UInt8),
        ("42 u16", Type.UInt16),
        ("42 u32", Type.UInt32),
        ("42 u64", Type.UInt64),
    ],
)
def test_float_operand(parser, test_input, expected_type):
    tree = parser("int_operand").parse(test_input)
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTConstant)
    assert 42 == ast.value
    assert expected_type == ast.type_


@pytest.mark.parametrize(
    "test_input,expected_type",
    [
        ("4.2 f32", Type.Float32),
        ("4.2 f64", Type.Float64),
    ],
)
def test_float_operand(parser, test_input, expected_type):
    tree = parser("float_operand").parse(test_input)
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTConstant)
    assert 4.2 == ast.value
    assert expected_type == ast.type_


def test_str_operand_rule(parser):
    tree = parser("str_operand").parse('"test"')
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTString)
    assert "test" == ast.value
    assert 0 == ast.index
    assert 0 == ast_pass.string_pool.index("test")


def test_str_operand_already_defined(parser):
    tree = parser("str_operand").parse('"test"')
    ast_pass = ASTPass()
    ast_pass.string_pool.append("test")
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTString)
    assert "test" == ast.value
    assert 0 == ast.index
    assert 0 == ast_pass.string_pool.index("test")


def test_binding_rule(parser):
    tree = parser("binding").parse("test")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTSymbol)
    assert "test" == ast.symbol
