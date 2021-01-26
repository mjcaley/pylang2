from lark import Visitor

from ..ast import Type


class CalculateAddresses(Visitor):
    def __init__(self):
        self.current_address = 0
        self.symbol_table = {}
        super().__init__()

    def visit(self, tree):
        self.symbol_table = tree.symbol_table
        self.visit_topdown(tree)

    def start(self, _):
        self.current_address = 0

    def function(self, tree):
        tree.address = self.current_address

    def nullary_instruction(self, tree):
        tree.address = self.current_address
        self.current_address += 1

    def unary_instruction(self, tree):
        tree.address = self.current_address
        self.current_address += 1

    def label(self, tree):
        tree.address = self.current_address

    def int_operand(self, tree):
        operand_type = tree.constant.type_
        if operand_type in [Type.UInt8, Type.Int8]:
            self.current_address += 1
        elif operand_type in [Type.UInt16, Type.Int16]:
            self.current_address += 2
        elif operand_type in [Type.UInt32, Type.Int32]:
            self.current_address += 4
        elif operand_type in [Type.UInt64, Type.Int64]:
            self.current_address += 8

    def float_operand(self, tree):
        operand_type = tree.constant.type_
        if operand_type == Type.Float32:
            self.current_address += 4
        elif operand_type == Type.Float64:
            self.current_address += 8

    def str_operand(self, _):
        self.current_address += 4
