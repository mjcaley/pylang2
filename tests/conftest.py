import pytest
from lark import Lark

from pylang2.assembler.parser import grammar


@pytest.fixture
def parser():
    def inner(start_rule):
        return Lark(grammar, start=start_rule, parser="lalr")

    return inner
