import argparse

from pylang2.assembler.parser import parser
from pylang2.assembler.passes.to_ast import ToAST
from pylang2.assembler.passes.to_symbol_table import ToSymbolTableAST
from pylang2.assembler.passes.print_ast import PrintAST


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("FILE", help="File to parse")
    args = arg_parser.parse_args()

    with open(args.FILE, "r") as program:
        parse_tree = parser.parse(program.read())

    print("Parse Tree")
    print("----------")
    print(parse_tree.pretty())

    ast = ToAST.run_pass(parse_tree)
    print("AST")
    print("---")
    PrintAST.run_pass(ast)

    print("\nSymbol AST")
    print("----------")
    ast = ToSymbolTableAST.run_pass(ast)
    PrintAST.run_pass(ast)


if __name__ == "__main__":
    main()
