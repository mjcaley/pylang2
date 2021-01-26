from pylang2.assembler.ast import ErrorNode, SymbolNode, SymbolKind
from pylang2.assembler.parser import parser
from pylang2.assembler.passes.to_symbol_table import ToSymbolTable
from pylang2.assembler.passes.undefined_symbols import UndefinedSymbols


def test_start_rule():
    tree = parser.parse(
        """func test locals=0, args=0
            ret
            """
    )
    symbol_tree = ToSymbolTable().transform(tree)
    undefined_symbols_pass = UndefinedSymbols()
    result = undefined_symbols_pass.transform(symbol_tree)

    assert symbol_tree.symbol_table is result.symbol_table


def test_binding_rule():
    tree = SymbolNode("test", "binding", [], None)
    undefined_symbols_pass = UndefinedSymbols()
    undefined_symbols_pass.symbol_table["test"] = SymbolKind.Function
    result = undefined_symbols_pass.transform(tree)

    assert tree is result


def test_binding_rule_error_undefined():
    tree = SymbolNode("test", "binding", [], None)
    undefined_symbols_pass = UndefinedSymbols()
    result = undefined_symbols_pass.transform(tree)

    assert isinstance(result, ErrorNode)
    assert tree is result.children[0]
