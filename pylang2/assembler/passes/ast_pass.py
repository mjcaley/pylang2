from ...tree_transformer import TreeTransformerTopDown
from ..ast import *


class ASTPass(TreeTransformerTopDown):
    def definition(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        operand = tree.children[-1:]

        # Get definition values
        symbol = str(ident_token)

        return ASTStruct(symbol=symbol, children=operand)

    def struct(self, tree):
        # Get tokens
        ident_token = tree.children[0]
        types = tree.children[1].children

        # Get struct values
        symbol = str(ident_token)

        # Make node
        return ASTStruct(symbol=symbol, children=types, meta=tree.meta)

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

        # Make node
        return ASTFunction(
            symbol=symbol,
            num_locals=num_locals,
            num_args=num_args,
            children=statements,
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

        return ASTLabel(symbol=symbol, children=[], meta=tree.meta)

    def int_operand(self, tree):
        try:
            type_def = tree.children[1].type
        except IndexError:
            type_def = "i32"
        mapped_type = Type(type_def.lower())
        value = int(tree.children[0].value)

        return ASTConstant(
            data=tree.data, value=value, type_=mapped_type, meta=tree.meta
        )

    def float_operand(self, tree):
        type_def = tree.children[1].type
        mapped_type = Type(type_def.lower())
        value = float(tree.children[0].value)

        return ASTConstant(
            data=tree.data, value=value, type_=mapped_type, meta=tree.meta
        )

    def str_operand(self, tree):
        value = str(tree.children[0]).strip('"')

        return ASTString(value=value, meta=tree.meta)

    def binding(self, tree):
        symbol = str(tree.children[0])

        return ASTSymbol(symbol=symbol, meta=tree.meta)
