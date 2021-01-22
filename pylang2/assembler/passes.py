from functools import singledispatch, singledispatchmethod

from .ast import ASTRoot
from .symbol_table import SymbolTable, FunctionSymbol, ConstantSymbol, LabelSymbol, DefinitionSymbol, StructSymbol


class DetectCycles:
    @singledispatch
    def visit(node) -> None:
        pass

    @visit.register
    def visit(node: ASTRoot) -> None:
        # resolved: dict[str, list[str]] = dict()
        # cycles: dict[str, list[str]] = dict()
        # for symbol in node.symbols:
        #     if symbol in resolved:
        #         continue
        #     visited: list[str] = list()
        #     while symbol not in visited:
        #         visited.append(symbol)
        #         value = node.symbols[symbol]
        #         if isinstance(value, )
        pass
            

# dict of symbols -> values
# for key, value in dict:
#   if value is ASTOperand binding:
#       