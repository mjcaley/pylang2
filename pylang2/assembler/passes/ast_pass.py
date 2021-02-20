from ...tree_transformer import TreeTransformer
from ..ast import *


class ASTPass(TreeTransformer):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.function_scope = SymbolTable()
        self.string_pool = []

        self._struct_index = 0
        self._function_index = 0

        super().__init__()

    def start(self, tree):
        return ASTRoot(
            children=tree.children,
            symbol_table=self.symbol_table,
            string_pool=self.string_pool,
            meta=tree.meta,
        )

    def definition(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        operand = tree.children[1]

        # Get definition values
        symbol = str(ident_token)

        if operand.type_ in (
            Type.UInt8,
            Type.UInt16,
            Type.UInt32,
            Type.UInt64,
            Type.Int8,
            Type.Int16,
            Type.Int32,
            Type.Int64,
            Type.Float32,
            Type.Float64,
        ):
            self.symbol_table.declare(
                symbol=symbol,
                kind=Kind.Constant,
                type_=operand.type_,
                value=operand.value,
            )
        elif operand.type_ == Type.String:
            self.symbol_table.declare(
                symbol=symbol,
                kind=Kind.String,
                type_=operand.type_,
                value=operand.value,
            )
        else:
            self.symbol_table.declare(symbol=symbol, kind=Kind.Binding)

        return ASTDefinition(symbol=symbol, children=[operand])

    def struct(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        types = tree.children[1]

        # Get struct values
        symbol = str(ident_token)
        struct_index = self._struct_index
        self._struct_index += 1

        struct_node = ASTStruct(
            symbol=symbol, struct_index=struct_index, children=types, meta=tree.meta
        )

        if not self.symbol_table.is_declared(symbol):
            self.symbol_table.declare(
                symbol=symbol, kind=Kind.Struct, type_=Type.UInt64, value=struct_index
            )
            return struct_node
        else:
            return ErrorNode(
                message=f"{symbol} already declared",
                children=[struct_node],
                meta=tree.meta,
            )

    def types(self, tree):
        return [Type(token.value) for token in tree.children]

    def function(self, tree):
        # Get tokens
        ident_token, locals_token, args_token, _ = tree.children
        statements = tree.children[3:]

        # Get function values
        symbol = str(ident_token)
        num_locals = int(locals_token)
        num_args = int(args_token)
        function_index = self._function_index

        scope = self.function_scope
        self.function_scope = SymbolTable()
        function_node = ASTFunction(
            children=statements,
            symbol=symbol,
            num_locals=num_locals,
            num_args=num_args,
            index=function_index,
            meta=tree.meta,
            symbol_table=scope,
        )

        if not self.symbol_table.is_declared(symbol):
            self.symbol_table.declare(
                symbol=symbol,
                kind=Kind.Function,
                type_=Type.UInt64,
                value=function_index,
            )

            return function_node
        else:
            return ErrorNode(
                message=f"{symbol} already declared",
                children=[function_node],
                meta=tree.meta,
            )

    def nullary_instruction(self, tree):
        instruction_token = tree.children[0]

        return ASTInstruction(
            data=tree.data,
            instruction=Instruction(str(instruction_token)),
            children=[],
            meta=tree.meta,
        )

    def unary_instruction(self, tree):
        instruction_token = tree.children[0]

        return ASTInstruction(
            data=tree.data,
            instruction=Instruction(str(instruction_token)),
            children=tree.children[1:],
            meta=tree.meta,
        )

    def label(self, tree):
        ident_token = tree.children[0]
        symbol = str(ident_token)

        label_node = ASTLabel(symbol=symbol, children=[], meta=tree.meta)

        if not self.function_scope.is_declared(symbol):
            self.function_scope.declare(
                symbol=symbol, kind=Kind.Label, type_=Type.UInt64
            )
            return label_node
        else:
            return ErrorNode(
                message=f"{symbol} is already declared",
                children=[label_node],
                meta=tree.meta,
            )

    def int_operand(self, tree):
        try:
            type_def = tree.children[1].type
        except IndexError:
            type_def = "i32"
        mapped_type = Type(type_def.lower())
        value = int(tree.children[0].value)

        return ASTInteger(value=value, type_=mapped_type, meta=tree.meta)

    def float_operand(self, tree):
        type_def = tree.children[1].type
        mapped_type = Type(type_def.lower())
        value = float(tree.children[0].value)

        return ASTFloat(value=value, type_=mapped_type, meta=tree.meta)

    def str_operand(self, tree):
        value = str(tree.children[0]).strip('"')
        if value not in self.string_pool:
            self.string_pool.append(value)
        index = self.string_pool.index(value)

        return ASTString(value=index, string_value=value, meta=tree.meta)

    def binding(self, tree):
        symbol = str(tree.children[0])

        return ASTSymbol(symbol=symbol, meta=tree.meta)
