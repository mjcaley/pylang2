from lark import Token, Tree, Discard
from lark.visitors import GrammarError, VisitError


class TreeTransformer:
    """A transformer that doesn't discard the Tree object."""

    def __init__(self, visit_tokens=True):
        self.visit_tokens = visit_tokens

    def _transform(self, node):
        try:
            if isinstance(node, Tree):
                return self._transform_tree(node)
            else:
                return self._transform_token(node)
        except Discard:
            pass

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
        children = [self._transform(child) for child in tree.children if child is not None]
        tree.children = children

        try:
            rule = getattr(self, tree.data)
        except AttributeError:
            return tree

        return rule(tree)

    def transform(self, tree: Tree):
        return self._transform(tree)
