import pytest

from pylang2.assembler.ast import (
    ASTDefinition,
    ASTFunction,
    ASTLabel,
    ASTOperand,
    ASTStruct,
    ASTSymbolFunction,
    ASTRoot,
    ASTSymbolTableRoot,
    ConstantSymbol,
    FunctionSymbol,
    LabelSymbol,
    Constant,
    StructSymbol,
    Type,
    ASTNullaryInstruction,
    Instruction,
)
from pylang2.assembler.passes.to_symbol_table import ToSymbolTableAST


def test_default_values():
    t = ToSymbolTableAST()

    assert None is not t.constants
    assert None is not t.symbols


def test_run_pass_returns_node():
    root = ASTRoot(
        [
            ASTDefinition(
                "test_def", ASTOperand(Constant(Type.String, "string"), 1, 2), 1, 1
            ),
            ASTStruct("test_struct", [Type.Int32], 2, 1),
            ASTFunction(
                "test_func", 0, 0, [ASTNullaryInstruction(Instruction.Ret, 4, 1)], 3, 1
            ),
        ]
    )
    result = ToSymbolTableAST.run_pass(root)

    assert isinstance(result, ASTSymbolTableRoot)


def test_start_returns_node():
    t = ToSymbolTableAST()
    root = ASTRoot(
        [
            ASTDefinition(
                "test_def", ASTOperand(Constant(Type.String, "string"), 1, 2), 1, 1
            ),
            ASTStruct("test_struct", [Type.Int32], 2, 1),
            ASTFunction(
                "test_func", 0, 0, [ASTNullaryInstruction(Instruction.Ret, 4, 1)], 3, 1
            ),
        ]
    )
    result = t.transform(root)

    assert isinstance(result, ASTSymbolTableRoot)
    assert all([isinstance(node, ASTSymbolFunction) for node in result.functions])


def test_definition_returns_none():
    t = ToSymbolTableAST()
    constant = Constant(Type.Int32, 42)
    definition = ASTDefinition("test", ASTOperand(constant, 1, 2), 1, 2)
    result = t.transform(definition)

    assert None is result


@pytest.mark.parametrize("test_input", [
    Constant(Type.Int64, 42),
    Constant(Type.UInt64, 42),
    Constant(Type.Float64, 4.2),
    Constant(Type.Address, 42),
    Constant(Type.String, "string"),
])
def test_definition_big_constants_added_to_constants(test_input):
    t = ToSymbolTableAST()
    constant = test_input
    definition = ASTDefinition("test", ASTOperand(constant, 1, 2), 1, 2)
    result = t.transform(definition)

    assert constant in t.constants


@pytest.mark.parametrize("test_input", [
    Constant(Type.Int8, 42),
    Constant(Type.Int16, 42),
    Constant(Type.Int32, 42),
    Constant(Type.UInt8, 42),
    Constant(Type.UInt16, 42),
    Constant(Type.UInt32, 42),
    Constant(Type.Float32, 4.2),
])
def test_definition_small_constants_not_added_to_constants(test_input):
    t = ToSymbolTableAST()
    constant = test_input
    definition = ASTDefinition("test", ASTOperand(constant, 1, 2), 1, 2)
    result = t.transform(definition)

    assert constant not in t.constants


def test_definition_added_to_symbols():
    t = ToSymbolTableAST()
    constant = Constant(Type.Int32, 42)
    definition = ASTDefinition("test", ASTOperand(constant, 1, 2), 1, 2)
    result = t.transform(definition)

    assert "test" in t.symbols
    assert isinstance(t.symbols["test"], ConstantSymbol)
    assert constant is t.symbols["test"].constant


def test_struct_returns_none():
    t = ToSymbolTableAST()
    name = Constant(Type.String, "test")
    struct = ASTStruct("test", [Type.Int32], 1, 2)
    result = t.transform(struct)

    assert None is result


def test_struct_name_added_to_constants():
    t = ToSymbolTableAST()
    name = Constant(Type.String, "test")
    struct = ASTStruct("test", [Type.Int32], 1, 2)
    result = t.transform(struct)

    assert name in t.constants


def test_struct_added_to_symbols():
    t = ToSymbolTableAST()
    name = Constant(Type.String, "test")
    struct = ASTStruct("test", [Type.Int32], 1, 2)
    result = t.transform(struct)

    assert "test" in t.symbols
    assert isinstance(t.symbols["test"], StructSymbol)
    assert struct.types == t.symbols["test"].types


def test_function_returns_node():
    t = ToSymbolTableAST()
    name = Constant(Type.String, "test")
    function = ASTFunction("test", 1, 2, [42], 3, 4)
    result = t.transform(function)

    assert isinstance(result, ASTSymbolFunction)
    assert "test" == result.name
    assert [42] == result.statements


def test_function_name_added_to_constants():
    t = ToSymbolTableAST()
    name = Constant(Type.String, "test")
    function = ASTFunction("test", 1, 2, [42], 3, 4)
    result = t.transform(function)

    assert name in t.constants


def test_function_added_to_symbols():
    t = ToSymbolTableAST()
    name = Constant(Type.String, "test")
    function = ASTFunction("test", 1, 2, [42], 3, 4)
    result = t.transform(function)

    assert "test" in t.symbols
    assert isinstance(t.symbols["test"], FunctionSymbol)
    assert name == t.symbols["test"].name
    assert 1 == t.symbols["test"].num_locals
    assert 2 == t.symbols["test"].num_args


def test_label_returns_none():
    t = ToSymbolTableAST()
    label = ASTLabel("test", 1, 2)
    result = t.transform(label)

    assert None is result


def test_label_added_to_symbols():
    t = ToSymbolTableAST()
    label = ASTLabel("test", 1, 2)
    result = t.transform(label)

    assert "test" in t.symbols
    assert isinstance(t.symbols["test"], LabelSymbol)
