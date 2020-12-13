import pytest

from pylang2.assembler.passes.bindings_to_constants import BindingsToConstants
from pylang2.assembler.ast import (
    ASTSymbolTableRoot,
    ASTSymbolFunction,
    ASTNullaryInstruction,
    ASTUnaryInstruction,
    ASTOperand,
    Constant,
    ConstantSymbol,
    Type,
    Instruction,
)


@pytest.fixture
def forty_two():
    return Constant(Type.Int32, 42)


@pytest.fixture
def tree():
    forty_two = Constant(Type.Int32, 42)
    return ASTSymbolTableRoot(
        {"forty_two": ConstantSymbol(forty_two)},
        {forty_two},
        [
            ASTSymbolFunction(
                "function",
                [
                    ASTUnaryInstruction(
                        Instruction.LdConst, ASTOperand(forty_two, 1, 1), 1, 1
                    ),
                    ASTUnaryInstruction(
                        Instruction.LdConst, ASTOperand("forty_two", 1, 1), 1, 1
                    ),
                    ASTNullaryInstruction(Instruction.Ret, 1, 1),
                ],
            ),
        ],
    )


def test_symbol_replaced_by_constant(tree):
    result = BindingsToConstants.run_pass(tree)

    assert isinstance(result, ASTSymbolTableRoot)


def test_transform_returns_argument(forty_two):
    b = BindingsToConstants()
    result = b.transform(forty_two)

    assert forty_two is result


def test_transform_root_adds_symbols(tree):
    b = BindingsToConstants()
    result = b.transform(tree)

    assert isinstance(result, ASTSymbolTableRoot)
    assert tree.symbol_table == b.symbols


def test_transform_function_returns_self():
    b = BindingsToConstants()
    result = b.transform(ASTSymbolFunction("test", []))

    assert isinstance(result, ASTSymbolFunction)


def test_transform_unary_instruction_returns_self_with_changed_operand(forty_two):
    b = BindingsToConstants()
    b.symbols["test"] = ConstantSymbol(forty_two)
    result = b.transform(
        ASTUnaryInstruction(Instruction.LdConst, ASTOperand("test", 1, 1), 1, 1)
    )

    assert forty_two == result.operand.value


def test_transform_operand_constant_doesnt_change(forty_two):
    b = BindingsToConstants()
    test_input = ASTOperand(forty_two, 1, 1)
    result = b.transform(test_input)

    assert forty_two == test_input.value


def test_transform_operand_binding_replaced_by_constant(forty_two):
    b = BindingsToConstants()
    b.symbols["test"] = ConstantSymbol(forty_two)
    test_input = ASTOperand("test", 1, 1)
    result = b.transform(test_input)

    assert forty_two == result.value


def test_transform_string(forty_two):
    b = BindingsToConstants()
    b.symbols["test"] = ConstantSymbol(forty_two)
    result = b.transform("test")

    assert forty_two == result
