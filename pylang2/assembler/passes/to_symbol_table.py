from lark import Transformer, v_args

from ..ast import (
    Constant,
    SymbolType,
    ErrorNode,
    LabelNode,
    StructNode,
    FunctionNode,
    InstructionNode,
    ConstantNode,
    SymbolNode,
    Type,
    Instruction,
)


@v_args(tree=True)
class ToSymbolTable(Transformer):
    def __init__(self):
        self.symbol_table: dict[str, SymbolType] = dict()
        self.constants: set[Constant] = set()
        super().__init__(visit_tokens=True)

    def definition(self, tree):
        ident_token, operand = tree.children
        symbol = str(ident_token)

        if symbol not in self.symbol_table:
            if isinstance(operand, ConstantNode):
                self.symbol_table[symbol] = SymbolType.Constant
            else:
                self.symbol_table[symbol] = SymbolType.Unknown
        else:
            return ErrorNode(f"{symbol} already defined", [tree], tree.meta)

        return SymbolNode(symbol, tree.data, tree.children, tree.meta)

    def struct(self, tree):
        ident_token = tree.children[0]
        symbol = str(ident_token)
        types = tree.children[1].children

        name = Constant(Type.String, symbol)
        self.constants.add(name)

        if symbol not in self.symbol_table:
            self.symbol_table[symbol] = SymbolType.Struct
            return StructNode(symbol, name, tree.data, types, tree.meta)
        else:
            return ErrorNode(f"{symbol} already defined", [tree], tree.meta)

    def function(self, tree):
        ident_token, locals_token, args_token, statements = tree.children

        symbol = str(ident_token)
        symbol_constant = Constant(Type.String, symbol)
        self.constants.add(symbol_constant)

        if symbol not in self.symbol_table:
            self.symbol_table[symbol] = SymbolType.Function
        else:
            return ErrorNode(f"{symbol} already defined", [tree], tree.meta)

        return FunctionNode(
            symbol,
            symbol_constant,
            int(locals_token),
            int(args_token),
            tree.data,
            statements,
            tree.meta,
        )

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

        node = LabelNode(name, tree.data, tree.children, tree.meta)
        if name not in self.symbol_table:
            self.symbol_table[name] = SymbolType.Label
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
        self.constants.add(constant)

        return ConstantNode(constant, tree.data, [], tree.meta)

    def float_operand(self, tree):
        type_def = tree.children[1].type
        mapped_type = Type(type_def.lower())
        value_token = tree.children[0]

        constant = Constant(mapped_type, float(value_token.value))
        self.constants.add(constant)

        return ConstantNode(constant, tree.data, [], tree.meta)

    def str_operand(self, tree):
        value_token = str(tree.children[0]).strip('"')

        constant = Constant(Type.String, value_token)
        self.constants.add(constant)

        return ConstantNode(constant, tree.data, [], tree.meta)

    def binding(self, tree):
        symbol = str(tree.children[0])

        return SymbolNode(symbol, tree.data, tree.children, tree.meta)
