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
            ldlocal 0
            ldlocal 1
            add i32
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
    assert "dec_integer" == result.children[2].data


def test_parses_function(parser):
    result = parser("function").parse(
        """
        func add locals=2, args=2
            ldlocal 0
            ldlocal 1
            add i32
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
        ("ldlocal 42", "instruction"),
        ("label_name:", "label"),
    ],
)
def test_parses_statement(parser, test_input, expected):
    result = parser("statements").parse(test_input)

    assert expected == result.children[0].data


@pytest.mark.parametrize(
    "test_input,expected_instruction",
    [
        ("halt", "HALT"),
        ("noop", "NOOP"),
        ("pop", "POP"),
        ("ret", "RET"),
    ],
)
def test_parses_void_nullary_instruction_none_parameter(
    parser, test_input, expected_instruction
):
    result = parser("instruction").parse(test_input)

    assert expected_instruction == result.children[0].type
    assert None is result.children[1]


@pytest.mark.parametrize(
    "test_input,expected_instruction,expected_type",
    [
        ("halt void", "HALT", "VOID"),
        ("noop void", "NOOP", "VOID"),
        ("pop void", "POP", "VOID"),
        ("ret void", "RET", "VOID"),
    ],
)
def test_parses_void_nullary_instruction_void_parameter(
    parser, test_input, expected_instruction, expected_type
):
    result = parser("instruction").parse(test_input)

    assert expected_instruction == result.children[0].type
    assert expected_type == result.children[1].type


@pytest.mark.parametrize(
    "test_input,expected_instruction",
    [
        ("testeq", "TESTEQ"),
        ("testne", "TESTNE"),
        ("testgt", "TESTGT"),
        ("testlt", "TESTLT"),
    ],
)
def test_byte_nullary_instruction_none_parameter(
    parser, test_input, expected_instruction
):
    result = parser("instruction").parse(test_input)

    assert expected_instruction == result.children[0].type
    assert None is result.children[1]


@pytest.mark.parametrize(
    "test_input,expected_instruction,expected_type",
    [
        ("testeq u8", "TESTEQ", "U8"),
        ("testne u8", "TESTNE", "U8"),
        ("testgt u8", "TESTGT", "U8"),
        ("testlt u8", "TESTLT", "U8"),
    ],
)
def test_byte_nullary_instruction_u8_parameter(
    parser, test_input, expected_instruction, expected_type
):
    result = parser("instruction").parse(test_input)

    assert expected_instruction == result.children[0].type
    assert expected_type == result.children[1].type


@pytest.mark.parametrize(
    "test_input,expected_instruction",
    [
        ("callvirt", "CALLVIRT"),
    ],
)
def test_index_nullary_instruction_none_parameter(
    parser, test_input, expected_instruction
):
    result = parser("instruction").parse(test_input)

    assert expected_instruction == result.children[0].type
    assert None is result.children[1]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("callvirt u64", "CALLVIRT"),
    ],
)
def test_index_nullary_instruction_u64_parameter(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert "U64" == result.children[1].type


@pytest.mark.parametrize(
    "test_input,expected_instruction,expected_type",
    [
        ("add i32", "ADD", "I32"),
        ("sub i32", "SUB", "I32"),
        ("mul i32", "MUL", "I32"),
        ("div i32", "DIV", "I32"),
        ("mod i32", "MOD", "I32"),
    ],
)
def test_typed_nullary_instruction(
    parser, test_input, expected_instruction, expected_type
):
    result = parser("instruction").parse(test_input)

    assert expected_instruction == result.children[0].type
    assert expected_type == result.children[1].type


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("ldlocal 42", "LDLOCAL"),
        ("stlocal 42", "STLOCAL"),
        ("jmp 42", "JMP"),
        ("jmpt 42", "JMPT"),
        ("jmpf 42", "JMPF"),
        ("callfunc 42", "CALLFUNC"),
        ("ldfield 42", "LDFIELD"),
        ("stfield 42", "STFIELD"),
        ("ldelem 42", "LDELEM"),
        ("stelem 42", "STELEM"),
    ],
)
def test_index_unary_instruction(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert None is result.children[1]
    assert None is not result.children[2]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("ldlocal u64 42", "LDLOCAL"),
        ("stlocal u64 42", "STLOCAL"),
        ("jmp u64 42", "JMP"),
        ("jmpt u64 42", "JMPT"),
        ("jmpf u64 42", "JMPF"),
        ("callfunc u64 42", "CALLFUNC"),
        ("ldfield u64 42", "LDFIELD"),
        ("stfield u64 42", "STFIELD"),
        ("ldelem u64 42", "LDELEM"),
        ("stelem u64 42", "STELEM"),
    ],
)
def test_index_unary_instruction_with_u64_parameter(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert "U64" == result.children[1].type
    assert None is not result.children[2]


@pytest.mark.parametrize("test_input,expected", [
    ("newstruct 42", "NEWSTRUCT"),
    ("newarray 42", "NEWARRAY")
])
def test_address_unary_instruction_with_none_parameter(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert None is result.children[1]
    assert None is not result.children[2]


@pytest.mark.parametrize("test_input,expected", [
    ("newstruct addr 42", "NEWSTRUCT"),
    ("newarray addr 42", "NEWARRAY")
])
def test_address_unary_instruction_with_addr_parameter(parser, test_input, expected):
    result = parser("instruction").parse(test_input)

    assert expected == result.children[0].type
    assert "ADDR" == result.children[1].type
    assert None is not result.children[2]


def test_typed_unary_instruction(parser):
    result = parser("instruction").parse("ldconst i32 42")

    assert "LDCONST" == result.children[0].type
    assert "I32" == result.children[1].type
    assert None is not result.children[2]


def test_parses_label(parser):
    result = parser("label").parse("label_name:")

    assert "label_name" == result.children[0].value
    assert "CNAME" == result.children[0].type


@pytest.mark.parametrize(
    "test_input,expected_sign,expected_literal",
    [
        ("+42", "+", "42"),
        ("-42", "-", "42"),
        ("-4.2", "-", "4.2"),
        ("-4.2", "-", "4.2"),
    ],
)
def test_parses_number_literal_with_sign(
    parser, test_input, expected_sign, expected_literal
):
    result = parser("number_literal").parse(test_input)

    assert expected_sign == result.children[0].value
    assert expected_literal == result.children[1].children[0].value


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
