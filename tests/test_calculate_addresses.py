import pytest

from pylang2.assembler.ast import SymbolTableNode
from pylang2.assembler.parser import parser
from pylang2.assembler.passes.calculate_addresses import CalculateAddresses
from pylang2.assembler.passes.to_symbol_table import ToSymbolTable


def test_visit(mocker):
    calculate_addresses_pass = CalculateAddresses()
    visit_topdown_spy = mocker.spy(calculate_addresses_pass, 'visit_topdown')
    tree = SymbolTableNode("mock", [])
    calculate_addresses_pass.visit(tree)

    assert visit_topdown_spy.called


def test_init():
    calculate_addresses_pass = CalculateAddresses()

    assert 0 == calculate_addresses_pass.current_address


def test_start_rule():
    tree = parser.parse("")
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    assert 0 == calculate_addresses_pass.current_address


def test_function_rule():
    tree = parser.parse("""
        func test1 locals=0, args=0
            ret
        func test2 locals=0, args=0
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    assert 0 == symbol_tree.children[0].address
    assert 1 == symbol_tree.children[1].address


def test_nullary_instruction_rule():
    tree = parser.parse("""
        func test locals=0, args=0
            noop
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    test_instructions = symbol_tree.children[0].children[0].children
    assert 0 == test_instructions[0].address
    assert 1 == test_instructions[1].address


@pytest.mark.parametrize("test_input,expected", [
    ("ldconst 40 i8", 2)
])
def test_unary_instruction_rule(test_input, expected):
    tree = parser.parse(f"""
        func test locals=0, args=0
            {test_input}
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    test_instructions = symbol_tree.children[0].children[0].children
    assert 0 == test_instructions[0].address
    assert expected == test_instructions[1].address


def test_label_rule():
    tree = parser.parse(f"""
        func function locals=0, args=0
            noop
            test:
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    test_instructions = symbol_tree.children[0].children[0].children
    assert 1 == test_instructions[1].address


@pytest.mark.parametrize("test_input,expected", [
    ("ldconst 42 i8", 2),
    ("ldconst 42 i16", 3),
    ("ldconst 42 i32", 5),
    ("ldconst 42 i64", 9),
    ("ldconst 42 u8", 2),
    ("ldconst 42 u16", 3),
    ("ldconst 42 u32", 5),
    ("ldconst 42 u64", 9),
])
def test_int_operand_rule(test_input, expected):
    tree = parser.parse(f"""
        func test locals=0, args=0
            {test_input}
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    test_instructions = symbol_tree.children[0].children[0].children
    assert expected == test_instructions[1].address


@pytest.mark.parametrize("test_input,expected", [
    ("ldconst 42.0 f32", 5),
    ("ldconst 42.0 f64", 9),
])
def test_float_operand_rule(test_input, expected):
    tree = parser.parse(f"""
        func test locals=0, args=0
            {test_input}
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    test_instructions = symbol_tree.children[0].children[0].children
    assert expected == test_instructions[1].address


def test_str_operand_rule():
    tree = parser.parse(f"""
        func test locals=0, args=0
            ldconst "test"
            ret
    """)
    symbol_tree = ToSymbolTable().transform(tree)
    calculate_addresses_pass = CalculateAddresses()
    calculate_addresses_pass.visit_topdown(symbol_tree)

    test_instructions = symbol_tree.children[0].children[0].children
    assert 5 == test_instructions[1].address
