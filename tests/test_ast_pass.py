import pytest

from pylang2.assembler.passes.ast_pass import ASTPass
from pylang2.assembler.ast import *


def test_start_rule(parser):
    tree = parser("start").parse(
    """
    define test1 i32 = 42
    func test2 locals=1, args=2
        ret
    """
    )
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTRoot)
    assert ast_pass.symbol_table == ast.symbol_table
    assert ast_pass.string_pool == ast.string_pool


def test_definition_rule(parser):
    tree = parser("definition").parse("define test i32 = 42")
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


@pytest.mark.parametrize("test_input", [
    """func test locals=1, args=2
        ret""",
    """func test args=2, locals=1
        ret"""
])
def test_function_rule(parser, test_input):
    tree = parser("function").parse(test_input)
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTFunction)
    assert "test" == ast.symbol
    assert 1 == ast.num_locals
    assert 2 == ast.num_args


@pytest.mark.parametrize(
    "test_input,expected_instruction,expected_type",
    [
        ("halt", Instruction.Halt, Type.Void),
        ("halt void", Instruction.Halt, Type.Void),
        ("noop", Instruction.Noop, Type.Void),
        ("noop void", Instruction.Noop, Type.Void),
        ("pop", Instruction.Pop, Type.Void),
        ("pop void", Instruction.Pop, Type.Void),
        ("ret", Instruction.Ret, Type.Void),
        ("ret void", Instruction.Ret, Type.Void),
        ("testeq", Instruction.TestEQ, Type.UInt8),
        ("testeq u8", Instruction.TestEQ, Type.UInt8),
        ("testne", Instruction.TestNE, Type.UInt8),
        ("testne u8", Instruction.TestNE, Type.UInt8),
        ("testlt", Instruction.TestLT, Type.UInt8),
        ("testlt u8", Instruction.TestLT, Type.UInt8),
        ("testgt", Instruction.TestGT, Type.UInt8),
        ("testgt u8", Instruction.TestGT, Type.UInt8),
        ("callvirt", Instruction.CallVirt, Type.UInt64),
        ("callvirt u64", Instruction.CallVirt, Type.UInt64),
        ("add i32", Instruction.Add, Type.Int32),
        ("sub i32", Instruction.Sub, Type.Int32),
        ("mul i32", Instruction.Mul, Type.Int32),
        ("div i32", Instruction.Div, Type.Int32),
        ("mod i32", Instruction.Mod, Type.Int32),
        ("jmp 42", Instruction.Jmp, Type.UInt64),
        ("jmp u64 42", Instruction.Jmp, Type.UInt64),
        ("ldlocal 42", Instruction.LdLocal, Type.UInt64),
        ("ldlocal u64 42", Instruction.LdLocal, Type.UInt64),
        ("stlocal 42", Instruction.StLocal, Type.UInt64),
        ("stlocal u64 42", Instruction.StLocal, Type.UInt64),
        ("jmpt 42", Instruction.JmpT, Type.UInt64),
        ("jmpt u64 42", Instruction.JmpT, Type.UInt64),
        ("jmpf 42", Instruction.JmpF, Type.UInt64),
        ("jmpf u64 42", Instruction.JmpF, Type.UInt64),
        ("callfunc Symbol", Instruction.CallFunc, Type.UInt64),
        ("callfunc u64 Symbol", Instruction.CallFunc, Type.UInt64),
        ("newstruct Symbol", Instruction.NewStruct, Type.Address),
        ("newstruct addr 42", Instruction.NewStruct, Type.Address),
        ("ldfield 42", Instruction.LdField, Type.UInt64),
        ("ldfield u64 42", Instruction.LdField, Type.UInt64),
        ("stfield 42", Instruction.StField, Type.UInt64),
        ("stfield u64 42", Instruction.StField, Type.UInt64),
        ("newarray Symbol", Instruction.NewArray, Type.Address),
        ("newarray addr 42", Instruction.NewArray, Type.Address),
        ("ldelem 42", Instruction.LdElem, Type.UInt64),
        ("ldelem u64 42", Instruction.LdElem, Type.UInt64),
        ("stelem 42", Instruction.StElem, Type.UInt64),
        ("stelem u64 42", Instruction.StElem, Type.UInt64),
    ],
)
def test_instruction(parser, test_input, expected_instruction, expected_type):
    tree = parser("instruction").parse(test_input)
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTInstruction)
    assert expected_instruction == ast.instruction
    assert expected_type == ast.type_


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


def test_dec_integer(parser):
    tree = parser("dec_integer").parse("42")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTLiteral)
    assert "int_literal" == ast.data
    assert 42 == ast.value


def test_hex_integer(parser):
    tree = parser("hex_integer").parse("0x2a")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTLiteral)
    assert "int_literal" == ast.data
    assert 42 == ast.value


def test_bin_integer(parser):
    tree = parser("bin_integer").parse("0b00101010")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTLiteral)
    assert "int_literal" == ast.data
    assert 42 == ast.value


def test_float_literal(parser):
    tree = parser("float_literal").parse("4.2")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTLiteral)
    assert "float_literal" == ast.data
    assert 4.2 == ast.value


def test_string_literal_rule(parser):
    tree = parser("string_literal").parse('"test"')
    ast_pass = ASTPass()
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTLiteral)
    assert "string_literal" == ast.data
    assert 0 == ast.value
    assert 0 == ast_pass.string_pool.index("test")


def test_string_literal_already_defined(parser):
    tree = parser("string_literal").parse('"test"')
    ast_pass = ASTPass()
    ast_pass.string_pool.append("test")
    ast = ast_pass.transform(tree)

    assert isinstance(ast, ASTLiteral)
    assert "string_literal" == ast.data
    assert 0 == ast.value
    assert 0 == ast_pass.string_pool.index("test")


def test_binding_rule(parser):
    tree = parser("binding").parse("test")
    ast = ASTPass().transform(tree)

    assert isinstance(ast, ASTSymbol)
    assert "test" == ast.symbol
