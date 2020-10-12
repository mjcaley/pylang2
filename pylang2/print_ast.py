import argparse

from .assembler.parser import parser
from. assembler.ast import ToAST, ASTPrinter


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("FILE", help="File to parse")
    args = arg_parser.parse_args()

    with open(args.FILE, 'r') as program:
        parse_tree = parser.parse(program.read())
    to_ast = ToAST()
    untyped_ast = to_ast.transform(parse_tree)
    printer = ASTPrinter()
    printer.visit(untyped_ast)


if __name__ == "__main__":
    main()
