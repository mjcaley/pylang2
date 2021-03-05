from functools import singledispatchmethod

from lark import Visitor, v_args

from ..ast import *
from ...tree_transformer import TreeTransformer


class ASTVirtualMachine:
    def __init__(self, tree):
        self.tree = tree
        self._definition_map = {
            item.symbol: item for item in tree.find_data("definition")
        }
        self._stack = []

    def is_recursive(self):
        defined = set()
        for value in self._stack:
            if value in defined:
                return True
            else:
                defined.add(value)
        return False

    @singledispatchmethod
    def visit(self, tree):
        raise NotImplementedError

    @visit.register
    def _(self, tree: ASTDefinition):
        self._stack.append(tree.symbol)
        if self.is_recursive():
            raise RecursionError

        result = self.visit(tree.children[0])

        self._stack.pop()

        return result

    @visit.register
    def _(self, tree: ASTSymbol):
        return self.visit(self._definition_map[tree.symbol])

    @visit.register
    def _(self, tree: ASTInteger):
        return Symbol(kind=Kind.Constant, type_=tree.type_, value=tree.value)

    @visit.register
    def _(self, tree: ASTFloat):
        return Symbol(kind=Kind.Constant, type_=tree.type_, value=tree.value)

    @visit.register
    def _(self, tree: ASTString):
        return Symbol(kind=Kind.String, type_=tree.type_, value=tree.value)

    def run(self, definition: ASTDefinition):
        return self.visit(definition)


class Phase2(TreeTransformer):
    """AST pass that inserts addresses and resolves symbols."""

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.address = 0
        super().__init__()

    def start(self, tree):
        pass

    def definition(self, tree):
        pass
