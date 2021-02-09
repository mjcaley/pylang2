from typing import Iterator

from ...tree_transformer import TreeTransformer
from ..ast import Constant, FunctionNode, SymbolTableNode, SymbolKind


class CodeGeneration(TreeTransformer):
    def __init__(self):
        self.function_pool: dict[str, FunctionNode] = {}
        self.string_pool: dict[Constant, int] = {}
        super().__init__(visit_tokens=True)

    def start(self, tree: SymbolTableNode):
        # function_symbols = {symbol: value for symbol,value in tree.symbol_table.items() if value.kind == SymbolKind.Function }
        function_nodes: Iterator[FunctionNode] = tree.find_data("function")
        self.function_pool = None

    def function(self, tree):
        pass

