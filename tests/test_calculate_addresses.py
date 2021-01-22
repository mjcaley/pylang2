from pylang2.assembler.passes.calculate_addresses2 import CalculateAddresses





# import pytest

# from pylang2.assembler.passes.calculate_addresses import CalculateAddresses
# from pylang2.assembler.ast import (
#     ASTSymbolTableRoot,
#     ASTSymbolFunction,
#     ASTLabel,
#     ASTNullaryInstruction,
#     ASTUnaryInstruction,
#     ASTOperand,
#     FunctionSymbol,
#     LabelSymbol,
#     Constant,
#     Type,
#     Instruction,
# )


# @pytest.fixture
# def tree():
#     func_name = Constant(Type.String, "function")
#     return ASTSymbolTableRoot(
#         {
#             "function": FunctionSymbol(Constant(Type.String, "function"), 1, 1),
#             "label": LabelSymbol(),
#         },
#         {func_name},
#         [
#             ASTSymbolFunction(
#                 "function",
#                 [
#                     ASTUnaryInstruction(
#                         Instruction.LdConst,
#                         ASTOperand(Constant(Type.Int32, 42), 2, 4),
#                         2,
#                         12,
#                     ),
#                     ASTLabel("label", 3, 4),
#                     ASTNullaryInstruction(Instruction.Ret, 4, 4),
#                 ],
#             ),
#         ],
#     )


# def test_default_values(mocker):
#     c = CalculateAddresses(mocker.stub())

#     assert 0 == c.current_address


# def test_run_pass(tree):
#     result = CalculateAddresses.run_pass(tree)

#     assert 0 == result.symbol_table["function"].address
#     assert 5 == result.symbol_table["label"].address


# def test_root_returns_tree(tree):
#     c = CalculateAddresses(tree.symbol_table)
#     result = c.transform(tree)

#     assert 0 == result.symbol_table["function"].address
#     assert 5 == result.symbol_table["label"].address


# def test_function_address_updated(mocker):
#     c = CalculateAddresses(mocker.stub())
#     c.symbols = {"test": FunctionSymbol(mocker.stub(), 1, 1)}
#     c.transform(ASTSymbolFunction("test", [mocker.stub()]))

#     assert 0 == c.symbols["test"].address


# def test_label_address_updated(mocker):
#     c = CalculateAddresses(mocker.stub())
#     c.symbols = {"test": LabelSymbol()}
#     c.transform(ASTLabel("test", 1, 1))

#     assert 0 == c.symbols["test"].address


# def test_nullary_instruction_increments_by_1(mocker):
#     c = CalculateAddresses(mocker.stub())
#     c.transform(ASTNullaryInstruction(mocker.stub(), 1, 1))

#     assert 1 == c.current_address


# def test_unary_instruction_increments_by_5(mocker):
#     c = CalculateAddresses(mocker.stub())
#     c.transform(ASTUnaryInstruction(mocker.stub(), mocker.stub(), 1, 1))

#     assert 5 == c.current_address
