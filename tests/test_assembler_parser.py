import pytest


def test_parses_start(parser):
    result = parser("start").parse(
        """
        struct String
            u64,
            addr
    
        define FortyTwo i32 = 42
        define Error str = "Error occurred"
        
        func add locals=2, args=2
            ldlocal i32 0
            ldlocal i32 1
            add
            ret
    """
    )

    assert "struct" == result.children[0].data
    assert "definition" == result.children[1].data
    assert "definition" == result.children[2].data
    assert "function" == result.children[3].data


def test_parses_struct(parser):
    result = parser("struct").parse(
        """
        struct Object
            i32, u8, addr
    """
    )

    assert "Object" == result.children[0].value
    assert "I32" == result.children[1].type
    assert "U8" == result.children[2].type
    assert "ADDR" == result.children[3].type


def test_parses_definition(parser):
    result = parser("definition").parse("define test i32 = 42")

    assert "test" == result.children[0].value
    assert "42" == result.children[2].children[0].value


def test_parses_function(parser):
    result = parser("function").parse(
        """
        func add locals=2, args=2
            ldlocal i32 0
            ldlocal i32 1
            add
            ret
    """
    )

    assert "add" == result.children[0].value
    assert "2" == result.children[1].children[0].value
    assert "2" == result.children[2].children[0].value
    assert "statements" == result.children[3].data


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("noop", "instruction"),
        ("ldlocal i32 42", "instruction"),
        ("label_name:", "label"),
    ],
)
def test_parses_statement(parser, test_input, expected):
    result = parser("statements").parse(test_input)

    assert expected == result.children[0].data


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("halt", "HALT"),
        ("noop", "NOOP"),
        ("add", "ADD"),
        ("sub", "SUB"),
        ("mul", "MUL"),
        ("div", "DIV"),
        ("mod", "MOD"),
        ("pop", "POP"),
        ("jmp", "JMP"),
        ("jmpt", "JMPT"),
        ("jmpf", "JMPF"),
        ("testeq", "TESTEQ"),
        ("testne", "TESTNE"),
        ("testgt", "TESTGT"),
        ("testlt", "TESTLT"),
        ("callvirt", "CALLVIRT"),
        ("ret", "RET"),
    ],
)
def test_parses_nullary_instruction_without_type(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("halt void", "HALT"),
        ("noop void", "NOOP"),
        ("add void", "ADD"),
        ("sub void", "SUB"),
        ("mul void", "MUL"),
        ("div void", "DIV"),
        ("mod void", "MOD"),
        ("pop void", "POP"),
        ("jmp void", "JMP"),
        ("jmpt void", "JMPT"),
        ("jmpf void", "JMPF"),
        ("testeq void", "TESTEQ"),
        ("testne void", "TESTNE"),
        ("testgt void", "TESTGT"),
        ("testlt void", "TESTLT"),
        ("callvirt void", "CALLVIRT"),
        ("ret void", "RET"),
    ],
)
def test_parses_nullary_instruction_with_type(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert "VOID" == result.children[1].type


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("ldconst i32 42", "LDCONST"),
        ("ldlocal i32 42", "LDLOCAL"),
        ("stlocal i32 42", "STLOCAL"),
        ("callfunc i32 42", "CALLFUNC"),
        ("newstruct i32 42", "NEWSTRUCT"),
        ("ldfield i32 42", "LDFIELD"),
        ("stfield i32 42", "STFIELD"),
        ("newarray i32 42", "NEWARRAY"),
        ("ldelem i32 42", "LDELEM"),
        ("stelem i32 42", "STELEM"),
    ],
)
def test_parses_unary_instruction(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert "I32" == result.children[1].type
    assert "42" == result.children[2].children[0].value


def test_parses_label(parser):
    result = parser("label").parse("label_name:")

    assert "label_name" == result.children[0].value
    assert "CNAME" == result.children[0].type


def test_parses_dec_integer(parser):
    result = parser("dec_integer").parse("42")

    assert "INT" == result.children[0].type
    assert "42" == result.children[0].value


def test_parses_hex_integer(parser):
    result = parser("hex_integer").parse("0x42")

    assert "HEXADECIMAL" == result.children[0].type
    assert "42" == result.children[0].value


def test_parses_bin_integer(parser):
    result = parser("bin_integer").parse("0b1010")

    assert "BINARY" == result.children[0].type
    assert "1010" == result.children[0].value


def test_parses_float_literal(parser):
    result = parser("float_literal").parse(f"42.0")

    assert "DECIMAL" == result.children[0].type
    assert "42.0" == result.children[0].value


def test_parses_string_literal(parser):
    result = parser("string_literal").parse('"String value"')

    assert "ESCAPED_STRING" == result.children[0].type
    assert '"String value"' == result.children[0].value


def test_parses_binding(parser):
    result = parser("binding").parse("identifier")

    assert "identifier" == result.children[0].value
    assert "CNAME" == result.children[0].type
