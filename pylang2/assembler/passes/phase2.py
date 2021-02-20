from functools import singledispatchmethod

from lark import Visitor, v_args

from ..ast import *


class ASTVirtualMachine:
    def __init__(self, tree):
        self.tree = tree
        self.definitions = [definition for definition in tree.find_data("definition")]
        self.definition_map = {item.symbol: item for item in self.definitions}
        self.stack = []

    def is_recursive(self):
        defined = set()
        for value in self.stack:
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
        self.stack.append(tree.symbol)
        if self.is_recursive():
            raise RecursionError

        result = self.visit(tree.children[0])

        self.stack.pop()

        return result

    @visit.register
    def _(self, tree: ASTSymbol):
        return self.visit(self.definition_map[tree.symbol])

    @visit.register
    def _(self, tree: ASTInteger):
        return Symbol(kind=Kind.Constant, type_=tree.type_, value=tree.value)

    @visit.register
    def _(self, tree: ASTFloat):
        return Symbol(kind=Kind.Constant, type_=tree.type_, value=tree.value)

    @visit.register
    def _(self, tree: ASTString):
        return Symbol(kind=Kind.String, type_=tree.type_, value=tree.value)

    def run(self):
        for definition in self.definitions:
            result = self.visit(definition)
            self.tree.symbol_table.update(definition.symbol, result.kind, result.type_, result.value)

        return self.tree


# class Phase2(Visitor):
#     """AST pass that inserts addresses and resolves symbols."""
#
#     def __init__(self, symbol_table):
#         self.symbol_table = symbol_table
#         self.address = 0
#         super().__init__()
#
#     @v_args(tree=True)
#     def start(self, tree):
#         pass
#
#     @v_args(tree=True)
#     def function(self, tree: ASTFunction):
#         tree.address = self.address
