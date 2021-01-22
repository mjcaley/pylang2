from ...tree_transformer import TreeTransformerInPlace


class CalculateAddresses(TreeTransformerInPlace):
    def __init__(self):
        self.current_address = 0
        super().__init__()

    def start(self, tree):
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

    def int_operand(self, _):
        self.current_address += 4

    def float_operand(self, _):
        self.current_address += 4

    def str_operand(self, _):
        self.current_address += 4

    def binding(self, _):
        self.current_address += 4
