import pytest

from pylang2.assembler.ast import ConstantNode, ErrorNode, Type, SymbolKind
from pylang2.assembler.parser import parser
from pylang2.assembler.passes.resolve_bindings import ResolveBindings
from pylang2.assembler.passes.to_symbol_table import ToSymbolTable


@pytest.fixture
def to_symbol_tree():
    def inner(program):
        tree = parser.parse(program)
        return ToSymbolTable().transform(tree)
    return inner


def test_binding_rule_constant(to_symbol_tree):
    tree = to_symbol_tree("""
        define test1 = 42 i32
    """)
    resolve_bindings_pass = ResolveBindings()
    resolved_tree = resolve_bindings_pass.transform(tree)

    node = resolved_tree.children[0].children[0]
    assert isinstance(node, ConstantNode)
    assert Type.Int32 == node.constant.type_
    assert 42 == node.constant.value
    assert SymbolKind.Constant == resolved_tree.symbol_table["test1"].kind
    assert Type.Int32 == resolved_tree.symbol_table["test1"].type_


def test_binding_rule_binding(to_symbol_tree):
    tree = to_symbol_tree("""
        define test1 = 42 i32
        define test2 = test1
    """)
    resolve_bindings_pass = ResolveBindings()
    resolved_tree = resolve_bindings_pass.transform(tree)

    node = resolved_tree.children[1].children[0]
    assert isinstance(node, ConstantNode)
    assert Type.Int32 == node.constant.type_
    assert 42 == node.constant.value
    assert SymbolKind.Constant == resolved_tree.symbol_table["test2"].kind
    assert Type.Int32 == resolved_tree.symbol_table["test2"].type_


def test_binding_rule_cycle(to_symbol_tree):
    tree = to_symbol_tree("""
        define test1 = test2
        define test2 = test1
    """)
    resolve_bindings_pass = ResolveBindings()
    resolved_tree = resolve_bindings_pass.transform(tree)

    node1 = resolved_tree.children[0].children[0]
    node2 = resolved_tree.children[1].children[0]
    assert isinstance(node1, ErrorNode)
    assert isinstance(node2, ErrorNode)


def test_binding_rule_doesnt_exist(to_symbol_tree):
    tree = to_symbol_tree("""
            define test1 = test2
        """)
    resolve_bindings_pass = ResolveBindings()
    resolved_tree = resolve_bindings_pass.transform(tree)

    node1 = resolved_tree.children[0].children[0]
    assert isinstance(node1, ErrorNode)
