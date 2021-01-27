from ..ast import Constant, FunctionNode


class ToAST(TreeTransformer):
    def __init__(self):
        self.function_pool: dict[str, FunctionNode] = {}
        self.string_pool: dict[Constant, int] = {}
        super().__init__(visit_tokens=True)

    def start(self, tree):
        #
        pass

    def function(self, tree):

