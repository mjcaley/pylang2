import pytest

from pylang2.assembler.passes.to_symbol_table import ToSymbolTable
from pylang2.assembler.ast import (
    SymbolTableValue,
    SymbolTableNode,
    ErrorNode,
    LabelNode,
    StructNode,
    FunctionNode,
    InstructionNode,
    SymbolNode,
    Type,
    SymbolKind,
    Instruction,
)


def test_start_rule(parser):
    tree = parser("start").parse(
        """
    func test locals=0, args=1
        ret
    """
    )
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, SymbolTableNode)
    assert symbol_table_pass.symbol_table is result.symbol_table
    assert symbol_table_pass.constants is result.constants


@pytest.mark.parametrize(
    "test_input,expected_kind,expected_type",
    [
        ("define test = 42 i32", SymbolKind.Constant, Type.Int32),
        ("define test = binding", SymbolKind.Unknown, None),
    ],
)
def test_definition_rule(parser, test_input, expected_kind, expected_type):
    tree = parser("definition").parse(test_input)
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, SymbolNode)
    assert "test" == result.symbol
    assert "test" in symbol_table_pass.symbol_table
    assert expected_kind == symbol_table_pass.symbol_table["test"].kind
    assert expected_type == symbol_table_pass.symbol_table["test"].type_


def test_definition_rule_error_already_defined(parser):
    tree = parser("definition").parse("define test = 42 i32")
    symbol_table_pass = ToSymbolTable()
    symbol_table_pass.symbol_table["test"] = SymbolTableValue(SymbolKind.Function, None)
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, ErrorNode)
    assert "definition" == result.children[0].data


def test_struct_rule(parser):
    tree = parser("struct").parse(
        """struct test
            i32
            f32
        """
    )
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert "test" in symbol_table_pass.symbol_table
    assert SymbolKind.Struct == symbol_table_pass.symbol_table["test"].kind
    assert None is symbol_table_pass.symbol_table["test"].type_
    assert isinstance(result, StructNode)
    assert "test" == result.symbol
    assert 0 == result.index
    assert 1 == symbol_table_pass.struct_index


def test_struct_rule_error_already_defined(parser):
    tree = parser("struct").parse(
        """struct test
            i32
            f32
        """
    )
    symbol_table_pass = ToSymbolTable()
    symbol_table_pass.symbol_table["test"] = SymbolTableValue(SymbolKind.Function, None)
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, ErrorNode)
    assert "struct" == result.children[0].data


def test_function_rule(parser):
    tree = parser("function").parse(
        """
    func test locals=1, args=2
        ret
    """
    )
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert "test" in symbol_table_pass.symbol_table
    assert SymbolKind.Function == symbol_table_pass.symbol_table["test"].kind
    assert None is symbol_table_pass.symbol_table["test"].type_
    assert isinstance(result, FunctionNode)
    assert "test" == result.symbol
    assert 1 == result.num_locals
    assert 2 == result.num_args
    assert None is result.address
    assert 0 == result.index
    assert 1 == symbol_table_pass.function_index


def test_function_rule_error_already_defined(parser):
    tree = parser("function").parse(
        """
    func test locals=1, args=2
        ret
    """
    )
    symbol_table_pass = ToSymbolTable()
    symbol_table_pass.symbol_table["test"] = SymbolTableValue(SymbolKind.Struct, None)
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, ErrorNode)
    assert "function" == result.children[0].data


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("halt", Instruction.Halt),
        ("noop", Instruction.Noop),
        ("add", Instruction.Add),
        ("sub", Instruction.Sub),
        ("mul", Instruction.Mul),
        ("div", Instruction.Div),
        ("mod", Instruction.Mod),
        ("pop", Instruction.Pop),
        ("jmp", Instruction.Jmp),
        ("jmpt", Instruction.JmpT),
        ("jmpf", Instruction.JmpF),
        ("testeq", Instruction.TestEQ),
        ("testne", Instruction.TestNE),
        ("testgt", Instruction.TestGT),
        ("testlt", Instruction.TestLT),
        ("callvirt", Instruction.CallVirt),
        ("ret", Instruction.Ret),
    ],
)
def test_nullary_instruction_rule(parser, test_input, expected):
    tree = parser("nullary_instruction").parse(test_input)
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, InstructionNode)
    assert expected == result.instruction


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("ldconst 42 i32", Instruction.LdConst),
        ("ldlocal 42 i32", Instruction.LdLocal),
        ("stlocal 42 i32", Instruction.StLocal),
        ("callfunc 42 i32", Instruction.CallFunc),
        ("newstruct 42 i32", Instruction.NewStruct),
        ("ldfield 42 i32", Instruction.LdField),
        ("stfield 42 i32", Instruction.StField),
        ("newarray 42 i32", Instruction.NewArray),
        ("ldelem 42 i32", Instruction.LdElem),
        ("stelem 42 i32", Instruction.StElem),
    ],
)
def test_unary_instruction_rule(parser, test_input, expected):
    tree = parser("unary_instruction").parse(test_input)
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, InstructionNode)
    assert expected == result.instruction


def test_label_rule(parser):
    tree = parser("label").parse("test:")
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert "test" in symbol_table_pass.symbol_table
    assert SymbolKind.Label == symbol_table_pass.symbol_table["test"].kind
    assert None is symbol_table_pass.symbol_table["test"].type_
    assert isinstance(result, LabelNode)
    assert "test" == result.symbol
    assert None is result.address


def test_label_rule_error_already_defined(parser):
    tree = parser("label").parse("test:")
    symbol_table_pass = ToSymbolTable()
    symbol_table_pass.symbol_table["test"] = SymbolTableValue(SymbolKind.Function, None)
    result = symbol_table_pass.transform(tree)

    assert isinstance(result, ErrorNode)
    assert isinstance(result.children[0], LabelNode)
    assert "label" == result.children[0].data


@pytest.mark.parametrize(
    "test_input,expected_type,expected_value",
    [
        ("42", Type.Int32, 42),
        ("-42", Type.Int32, -42),
        ("42 i8", Type.Int8, 42),
        ("42 i16", Type.Int16, 42),
        ("42 i32", Type.Int32, 42),
        ("42 i64", Type.Int64, 42),
        ("42 u8", Type.UInt8, 42),
        ("42 u16", Type.UInt16, 42),
        ("42 u32", Type.UInt32, 42),
        ("42 u64", Type.UInt64, 42),
    ],
)
def test_int_operand_rule(parser, test_input, expected_type, expected_value):
    tree = parser("int_operand").parse(test_input)
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert expected_type == result.constant.type_
    assert expected_value == result.constant.value
    assert result.constant in symbol_table_pass.constants


@pytest.mark.parametrize(
    "test_input,expected_type,expected_value",
    [
        ("42.0 f32", Type.Float32, 42.0),
        ("42.0 f64", Type.Float64, 42.0),
        ("-42.0 f32", Type.Float32, -42.0),
        ("-42.0 f64", Type.Float64, -42.0),
    ],
)
def test_float_operand_rule(parser, test_input, expected_type, expected_value):
    tree = parser("float_operand").parse(test_input)
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert expected_type == result.constant.type_
    assert pytest.approx(expected_value, result.constant.value)
    assert result.constant in symbol_table_pass.constants


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('"test"', "test"),
        ('"test" str', "test"),
    ],
)
def test_str_operand_rule(parser, test_input, expected):
    tree = parser("str_operand").parse(test_input)
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert Type.String == result.constant.type_
    assert expected == result.constant.value
    assert result.constant in symbol_table_pass.constants


def test_binding_rule(parser):
    tree = parser("binding").parse("test")
    symbol_table_pass = ToSymbolTable()
    result = symbol_table_pass.transform(tree)

    assert "test" == result.symbol
