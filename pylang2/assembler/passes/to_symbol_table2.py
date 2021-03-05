from lark import Visitor

from ...tree_transformer import TreeTransformer
from ..ast import *


class ToSymbolTable(TreeTransformer):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.string_pool = []
        self.struct_index = 0
        self.function_index = 0
        super().__init__()

    def _add_to_string_pool(self, string):
        try:
            index = self.string_pool.index(string)
        except ValueError:
            index = len(self.string_pool)
            self.string_pool.append(string)

        return index

    def definition(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        type_tokens = tree.children[1]

        # Get definition values
        symbol = str(ident_token)
        index = self.struct_index
        self.struct_index += 1
        types = []

        return ASTStruct(symbol, index, types)

    def struct(self, tree):
        tree.name_index = self._add_to_string_pool(tree.symbol)

        if not self.symbol_table.is_declared(tree.symbol):
            tree.index = self.struct_index
            self.struct_index += 1
            self.symbol_table.declare(
                tree.symbol, Kind.Struct, Type.UInt64, self.struct_index
            )
            return tree
        else:
            return ErrorNode(f"{tree.symbol} already defined", [tree], tree.meta)

    def function(self, tree):
        tree.name_index = self._add_to_string_pool(tree.symbol)
        tree.index = self.function_index
        self.function_index += 1

        if not self.symbol_table.is_declared(tree.symbol):
            self.symbol_table.declare(
                tree.symbol, Kind.Function, Type.UInt64, function_index
            )
            self.symbol_table.push_scope(tree.symbol)

            return tree
        else:
            return ErrorNode(f"{tree.symbol} already defined", [tree], tree.meta)

    def label(self, tree):
        if self.symbol_table.is_declared(tree.symbol):
            self.symbol_table.declare(tree.symbol, Kind.Label, Type.UInt64)

            return tree
        else:
            return ErrorNode(f"{tree.symbol} already defined", [tree], tree.meta)

    def str_operand(self, tree):
        try:
            index = self.string_pool.index(tree.value)
        except ValueError:
            index = len(self.string_pool)
            self.string_pool.append(tree.value)
        tree.index = index

        return tree
