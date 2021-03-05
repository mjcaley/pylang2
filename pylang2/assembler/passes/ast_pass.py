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
        type_ = Type(tree.children[1].value)
        operand = tree.children[2]

        # Get definition values
        symbol = str(ident_token)

        if type_ in (
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
                type_=type_,
                value=operand.value,
            )
        elif type_ == Type.String:
            self.symbol_table.declare(
                symbol=symbol,
                kind=Kind.String,
                type_=type_,
                value=operand.value,
            )
        else:
            self.symbol_table.declare(symbol=symbol, kind=Kind.Binding)

        return ASTDefinition(symbol=symbol, children=[operand])

    def struct(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        types = tree.children[1:]

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

    def function(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        param_tokens = {token.data: token.children[0] for token in tree.children[1:3]}
        statements = tree.children[3:]

        # Get function values
        symbol = str(ident_token)
        num_locals = int(param_tokens["locals"])
        num_args = int(param_tokens["args"])
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

    def instruction(self, tree):
        instruction_token = tree.children[0]
        type_token = tree.children[1]
        try:
            operand = [tree.children[2]]
        except IndexError:
            operand = []

        instruction = Instruction(instruction_token.value)

        if instruction in [
            Instruction.Halt,
            Instruction.Noop,
            Instruction.Pop,
            Instruction.Ret,
        ]:
            type_ = Type.Void
        elif instruction in [
            Instruction.TestEQ,
            Instruction.TestNE,
            Instruction.TestLT,
            Instruction.TestGT,
        ]:
            type_ = Type.UInt8
        elif instruction in [
            Instruction.Jmp,
            Instruction.JmpT,
            Instruction.JmpF,
            Instruction.CallVirt,
            Instruction.LdLocal,
            Instruction.StLocal,
            Instruction.CallFunc,
            Instruction.LdField,
            Instruction.StField,
            Instruction.LdElem,
            Instruction.StElem,
        ]:
            type_ = Type.UInt64
        elif instruction in [Instruction.NewStruct, Instruction.NewArray]:
            type_ = Type.Address
        else:
            type_ = Type(type_token.value)

        return ASTInstruction(
            children=operand, instruction=instruction, type_=type_, meta=tree.meta
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

    def dec_integer(self, tree):
        value = int(tree.children[0].value)

        return ASTLiteral(value=value, data="int_literal", meta=tree.meta)

    def hex_integer(self, tree):
        value = int(tree.children[0].value, base=16)

        return ASTLiteral(value=value, data="int_literal", meta=tree.meta)

    def bin_integer(self, tree):
        value = int(tree.children[0].value, base=2)

        return ASTLiteral(value=value, data="int_literal", meta=tree.meta)

    def float_literal(self, tree):
        value = float(tree.children[0].value)

        return ASTLiteral(value=value, data=tree.data, meta=tree.meta)

    def string_literal(self, tree):
        value = str(tree.children[0]).strip('"')
        if value not in self.string_pool:
            self.string_pool.append(value)
        index = self.string_pool.index(value)

        return ASTLiteral(value=index, data=tree.data, meta=tree.meta)

    def binding(self, tree):
        symbol = str(tree.children[0])

        return ASTSymbol(symbol=symbol, meta=tree.meta)

    def type(self, tree):
        return Type(tree.value)
