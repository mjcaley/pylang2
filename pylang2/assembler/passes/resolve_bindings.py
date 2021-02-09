# enter binding rule
# new set with binding VALUE
# VALUE = binding value
# while VALUE != Constant
#   VALUE = new binding value
#   if VALUE in set:
#       cycle detected
#       return ErrorNode
#   else: continue
# assign VALUE to all bindings in set

# Scenario 1: binding is constant
# define binding1 = 42 i32
#
# sees constants and doesn't enter the loop

# Scenario 2: binding is a symbol
# define binding1 = binding2
# define binding2 = 42 i32
#
# enters loop
# gets new value and adds to set
# gets constant to VALUE
# assigns all bindings in set the VALUE

from ...tree_transformer import TreeTransformer
from ..ast import Constant, Type, ErrorNode, ConstantNode, SymbolTableNode, SymbolKind, SymbolTableValue


class ResolveBindings(TreeTransformer):
    def __init__(self):
        self.definitions = {}
        self.nodes = {}
        self.symbol_table = {}
        self.constants = set()
        super().__init__()

    def transform(self, tree: SymbolTableNode):
        definitions = tree.find_data("definition")
        self.definitions = {definition.symbol: definition.children[0] for definition in definitions}
        self.nodes = {node.symbol: node for node in tree.find_pred(lambda t: t.data in ("definition", "function", "label"))}
        self.symbol_table = tree.symbol_table
        self.constants = tree.constants

        return super().transform(tree)

    def start(self, tree):
        tree.symbol_table = self.symbol_table
        tree.constants = self.constants

        return tree

    def definition(self, tree):
        child = tree.children[0]
        if isinstance(child, ConstantNode):
            self.symbol_table[tree.symbol] = SymbolTableValue(SymbolKind.Constant, child.constant.type_)

        return tree

    def binding(self, tree):
        visited = set()
        symbol = tree.symbol

        if symbol not in self.symbol_table:
            return ErrorNode(f"{symbol} is undefined", [tree], tree.meta)

        while symbol_value := self.symbol_table[symbol]:
            if symbol in visited:
                return ErrorNode(f"{symbol} is undefined", [tree], tree.meta)
            else:
                visited.add(symbol)

            if symbol_value.kind == SymbolKind.Unknown:
                symbol = self.nodes[symbol].children[0].value
            else:
                break

        self.symbol_table[tree.symbol] = symbol_value
        node = self.nodes[symbol]
        if symbol_value.kind == SymbolKind.Function:
            return ConstantNode(Constant(Type.UInt64, node.index), node.data, [], tree.meta)
        elif symbol_value.kind == SymbolKind.Constant:
            return ConstantNode(node.constant, node.data, [], tree.meta)
        elif symbol_value.kind == SymbolKind.Struct:
            return ConstantNode(node.index, node.data, [], tree.meta)
        elif symbol_value.kind == SymbolKind.Label:
            return ConstantNode(node.address, node.data, [], tree.meta)
        else:
            return ErrorNode(f"{symbol} cannot be resolved", [tree], tree.meta)
