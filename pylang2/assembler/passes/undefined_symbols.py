from ...tree_transformer import TreeTransformer
from ..ast import ErrorNode


class UndefinedSymbols(TreeTransformer):
    def __init__(self, visit_tokens=True):
        self.symbol_table = {}
        super().__init__(visit_tokens)

    def start(self, tree):
        self.symbol_table = tree.symbol_table

        return tree

    def binding(self, tree):
        if tree.symbol not in self.symbol_table:
            return ErrorNode(f"{tree.symbol} is undefined", [tree], tree.meta)
        else:
            return tree
