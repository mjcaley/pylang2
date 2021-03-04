from lark import Token, Tree, Discard
from lark.exceptions import GrammarError, VisitError


class TreeTransformer:
    """A transformer that doesn't discard the Tree object."""

    def __init__(self, visit_tokens=True):
        self.visit_tokens = visit_tokens

    def _transform(self, node):
        if isinstance(node, Tree):
            return self._transform_tree(node)
        elif isinstance(node, Token):
            return self._transform_token(node)
        else:
            return node

    def _transform_token(self, token: Token):
        if not self.visit_tokens:
            return token

        try:
            f = getattr(self, token.type)
        except AttributeError:
            return token

        if f is not None:
            try:
                return f(token)
            except (GrammarError, Discard):
                raise
            except Exception as e:
                raise VisitError(token.type, token, e) from e

    def _transform_tree(self, tree: Tree):
        children = [self._transform(child) for child in tree.children]
        tree.children = children

        try:
            rule = getattr(self, tree.data)
        except AttributeError:
            return tree

        return rule(tree)

    def transform(self, tree: Tree):
        return self._transform(tree)


class TreeTransformerTopDown(TreeTransformer):
    def __init__(self, visit_tokens=True):
        super().__init__(visit_tokens)

    def _transform_tree(self, tree: Tree):
        try:
            rule = getattr(self, tree.data)
        except AttributeError:
            return tree
        transformed_tree = rule(tree)

        children = [
            self._transform(child) for child in tree.children if child is not None
        ]
        transformed_tree.children = children

        return transformed_tree
