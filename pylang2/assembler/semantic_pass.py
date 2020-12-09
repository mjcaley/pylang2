from lark import Visitor, Token

from .errors import Redefinition, Undefined


class CheckRedefinitions(Visitor):
    def __init__(self, *args, **kwargs):
        self.symbols = set()
        self.errors = []
        super().__init__(*args, **kwargs)

    @staticmethod
    def run_pass(tree):
        check = CheckRedefinitions()
        check.visit(tree)

        return tree, check.errors

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


class UndefinedSymbols(Visitor):
    def __init__(self, *args, **kwargs):
        self.symbols = set()
        self.bindings = {}
        super().__init__(*args, **kwargs)

    @staticmethod
    def run_pass(tree):
        undef_pass = UndefinedSymbols()
        undef_pass.visit(tree)
        undefined = undef_pass.bindings.keys() - undef_pass.symbols
        errors = []
        for binding in undefined:
            errors.append(Undefined(binding, undef_pass.bindings[binding].line, undef_pass.bindings[binding].column))

        return tree, errors

    def definition(self, tree):
        self.symbols.add(tree.children[0])

    def struct(self, tree):
        self.symbols.add(tree.children[0])

    def function(self, tree):
        self.symbols.add(tree.children[0])

    def label(self, tree):
        self.symbols.add(tree.children[0])

    def binding(self, tree):
        self.bindings[tree.children[0].value] = tree
