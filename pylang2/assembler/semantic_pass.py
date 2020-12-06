from lark import Visitor, Token

from .errors import Redefinition


class CheckRedefinitions(Visitor):
    def __init__(self, *args, **kwargs):
        self.symbols = set()
        self.errors = []
        super().__init__(*args, **kwargs)

    def add_symbol(self, token: Token):
        if token.value in self.symbols:
            self.errors.append(Redefinition(token.value, token.line, token.column))
        else:
            self.symbols.add(token.value)

    def definition(self, tree):
        self.add_symbol(tree.children[0])

    def struct(self, tree):
        self.add_symbol(tree.children[0])

    def function(self, tree):
        self.add_symbol(tree.children[0])

    def label(self, tree):
        self.add_symbol(tree.children[0])
