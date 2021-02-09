from pathlib import Path

from lark import Lark

from .passes.to_ast import ASTPass


with open(Path(__file__).parent / "grammar.lark") as grammar_file:
    grammar = grammar_file.read()


parser = Lark(grammar, parser="lalr", propagate_positions=True, transformer=ASTPass())
