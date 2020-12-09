from pylang2.assembler.parser import parser
from pylang2.assembler.semantic_pass import CheckRedefinitions, UndefinedSymbols
from pylang2.assembler.errors import Redefinition, Undefined


def test_redefinition_in_definition():
    tree = parser.parse("""
    define forty_two = 42
    define forty_two = 42
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_in_struct():
    tree = parser.parse("""
    struct test
        i32
    struct test
        u64
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_in_function():
    tree = parser.parse("""
    func test locals=1, args=1
        ret
    func test locals=2, args=2
        ret
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_in_label():
    tree = parser.parse("""
    func test locals=1, args=1
        test:
        ret
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_can_be_collected():
    tree = parser.parse("""
    func test locals=1, args=1
        test:
        ret
    """)
    c = CheckRedefinitions()
    c.visit(tree)

    assert isinstance(c.errors[0], Redefinition)


def test_redefinition_run_pass():
    tree = parser.parse("""
    func test locals=0, args=0
        test:
        ret
    """)
    result = CheckRedefinitions.run_pass(tree)

    assert tree is result[0]
    assert isinstance(result[1][0], Redefinition)


def test_undefined_definition_added_to_symbols():
    tree = parser.parse("""
    define test = 42 i32
    """)
    u = UndefinedSymbols()
    u.visit(tree)

    assert "test" in u.symbols


def test_undefined_struct_added_to_symbols():
    tree = parser.parse("""
    struct test
        i32
    """)
    u = UndefinedSymbols()
    u.visit(tree)

    assert "test" in u.symbols


def test_undefined_function_added_to_symbols():
    tree = parser.parse("""
    func test locals=0, args=0
        ret
    """)
    u = UndefinedSymbols()
    u.visit(tree)

    assert "test" in u.symbols


def test_undefined_label_added_to_symbols():
    tree = parser.parse("""
    func one locals=0, args=0
        test:
        ret
    """)
    u = UndefinedSymbols()
    u.visit(tree)

    assert "test" in u.symbols


def test_undefined_binding_tree_added_to_bindings():
    tree = parser.parse("""
    define test = 42 i32

    func one locals=0, args=0
        ldconst test
        ret
    """)
    u = UndefinedSymbols()
    u.visit(tree)

    assert "test" in u.bindings


def test_undefined_run_pass():
    tree = parser.parse("""
    func one locals=0, args=0
        ldconst test
    """)
    result = UndefinedSymbols.run_pass(tree)

    assert tree is result[0]
    assert isinstance(result[1][0], Undefined)
