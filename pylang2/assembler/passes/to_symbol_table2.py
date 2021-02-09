from lark import Visitor

from ..ast import *


class ToSymbolTable(Visitor):
    def __init__(self):
        self.string_pool = []
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
        # Get tokens
        ident_token = tree.children[0]
        types = tree.children[1].children

        # Get struct values
        symbol = str(ident_token)
        name = Constant(Type.String, symbol)
        string_index = len(self.string_pool)
        self.string_pool.append(name)

        # Make node
        if not self.symbol_table.is_declared(symbol):
            index = self.struct_index
            self.struct_index += 1
            self.symbol_table.declare(symbol, Kind.Struct, Type.UInt64, self.struct_index)
            return ASTStruct(symbol, string_index, types, tree.meta, index)
        else:
            return ErrorNode(f"{symbol} already defined", [tree], tree.meta)

    def function(self, tree):
        # Get tokens
        ident_token, locals_token, args_token, _ = tree.children
        statements = tree.children[3:]

        # Get function values
        symbol = str(ident_token)
        string_index = self._add_to_string_pool(symbol)
        function_index = self.function_index
        self.function_index += 1

        # Make node
        if not self.symbol_table.is_declared(symbol):
            self.symbol_table.declare(symbol, Kind.Function, Type.UInt64, function_index)
            self.symbol_table.push_scope(symbol)
        else:
            return ErrorNode(f"{symbol} already defined", [tree], tree.meta)

        function_node = ASTFunction(
            symbol=symbol,
            name_index=string_index,
            num_locals=int(locals_token),
            num_args=int(args_token),
            index=function_index,
            children=statements,
            meta=tree.meta,
        )

        return function_node

    def nullary_instruction(self, tree):
        instruction_token = tree.children[0]

        return InstructionNode(
            Instruction(str(instruction_token)), tree.data, tree.children, tree.meta
        )

    def unary_instruction(self, tree):
        instruction_token = tree.children[0]

        return InstructionNode(
            Instruction(str(instruction_token)), tree.data, tree.children[1:], tree.meta
        )

    def label(self, tree):
        ident_token = tree.children[0]
        name = str(ident_token)

        node = LabelNode(name, tree.data, [], tree.meta)
        if self.symbol_table.is_declared(name):
            self.symbol_table.declare(name, Kind.Label, Type.UInt64)
            return node
        else:
            return ErrorNode(f"{name} already defined", [node], tree.meta)

    def int_operand(self, tree):
        try:
            type_def = tree.children[1].type
        except IndexError:
            type_def = "i32"
        mapped_type = Type(type_def.lower())
        value_token = tree.children[0]
        constant = Constant(mapped_type, int(value_token.value))

        return ConstantNode(constant, tree.data, [], tree.meta)

    def float_operand(self, tree):
        type_def = tree.children[1].type
        mapped_type = Type(type_def.lower())
        value_token = tree.children[0]
        constant = Constant(mapped_type, float(value_token.value))

        return ConstantNode(constant, tree.data, [], tree.meta)

    def str_operand(self, tree):
        value_token = str(tree.children[0]).strip('"')
        try:
            index = self.string_pool.index(value_token)
        except ValueError:
            index = len(self.string_pool)
            self.string_pool.append(value_token)
        constant = Constant(Type.String, value_token)

        return StringNode(constant, index, tree.data, [], tree.meta)

    def binding(self, tree):
        symbol = str(tree.children[0])

        return SymbolNode(symbol, tree.data, tree.children, tree.meta)
