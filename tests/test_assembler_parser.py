import pytest

from lark import Lark

from pylang2.assembler.parser import grammar


@pytest.fixture
def parser():
    def inner(start_rule):
        return Lark(grammar, start=start_rule, parser="lalr")

    return inner


def test_parses_start(parser):
    result = parser("start").parse(
        """
        struct String
            u64
            addr
    
        define FortyTwo = 42 i32
        define Error = "Error occurred" str
        
        func add locals=2, args=2
            ldlocal 0
            ldlocal 1
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
            i32
            u8
            addr
    """
    )

    assert "Object" == result.children[0].value
    assert "types" == result.children[1].data


def test_parses_types(parser):
    result = parser("types").parse(
        """
        i8
        i16
        i32
        i64
        u8
        u16
        u32
        u64
        f32
        f64
        str
        addr
    """
    )

    assert "i8" == result.children[0].value
    assert "i16" == result.children[1].value
    assert "i32" == result.children[2].value
    assert "i64" == result.children[3].value
    assert "u8" == result.children[4].value
    assert "u16" == result.children[5].value
    assert "u32" == result.children[6].value
    assert "u64" == result.children[7].value
    assert "f32" == result.children[8].value
    assert "f64" == result.children[9].value
    assert "str" == result.children[10].value
    assert "addr" == result.children[11].value


def test_parses_definition(parser):
    result = parser("definition").parse("define test = 42 i32")

    assert "test" == result.children[0].value
    assert "int_operand" == result.children[1].data


def test_parses_function(parser):
    result = parser("function").parse(
        """
        func add locals=2, args=2
            ldlocal 0
            ldlocal 1
            add
            ret
    """
    )

    assert "add" == result.children[0].value
    assert "2" == result.children[1].value
    assert "2" == result.children[2].value
    assert "statements" == result.children[3].data


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("noop", "nullary_instruction"),
        ("ldlocal 42 i32", "unary_instruction"),
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
def test_parses_nullary_instruction(parser, test_input, expected):
    result = parser("nullary_instruction").parse(test_input)

    assert expected == result.children[0].type


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("ldconst 42", "LDCONST"),
        ("ldlocal 42", "LDLOCAL"),
        ("stlocal 42", "STLOCAL"),
        ("callfunc 42", "CALLFUNC"),
        ("newstruct 42", "NEWSTRUCT"),
        ("ldfield 42", "LDFIELD"),
        ("stfield 42", "STFIELD"),
        ("newarray 42", "NEWARRAY"),
        ("ldelem 42", "LDELEM"),
        ("stelem 42", "STELEM"),
    ],
)
def test_parses_unary_instruction(parser, test_input, expected):
    result = parser("unary_instruction").parse(test_input)

    assert expected == result.children[0].type
    assert "int_operand" == result.children[1].data


def test_parses_label(parser):
    result = parser("label").parse("label_name:")

    assert "label_name" == result.children[0].value
    assert "CNAME" == result.children[0].type


# @pytest.mark.parametrize("test_input,expected", [
#     ("42 i32", "int_operand"),
#     ("42.0 f32", "float_operand"),
#     ('"A string" str', "str_operand"),
#     ("identifier", "binding"),
# ])
# def test_operand_returns_sub_rule(parser, test_input, expected):
#     result = parser("_operand").parse(test_input)
#
#     assert expected == result.data


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("i8", "I8"),
        ("i16", "I16"),
        ("i32", "I32"),
        ("i64", "I64"),
        ("u8", "U8"),
        ("u16", "U16"),
        ("u32", "U32"),
        ("u64", "U64"),
    ],
)
def test_parses_int_operand(parser, test_input, expected):
    result = parser("int_operand").parse(f"42 {test_input}")

    assert "SIGNED_INT" == result.children[0].type
    assert "42" == result.children[0].value
    assert expected == result.children[1].type


def test_parses_int_operand_without_type(parser):
    result = parser("int_operand").parse("42")

    assert "SIGNED_INT" == result.children[0].type
    assert "42" == result.children[0].value


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("f32", "F32"),
        ("f64", "F64"),
    ],
)
def test_parses_float_operand(parser, test_input, expected):
    result = parser("float_operand").parse(f"42.0 {test_input}")

    assert "SIGNED_FLOAT" == result.children[0].type
    assert "42.0" == result.children[0].value
    assert expected == result.children[1].type


def test_parses_string_operand(parser):
    result = parser("str_operand").parse('"String value" str')

    assert "ESCAPED_STRING" == result.children[0].type
    assert '"String value"' == result.children[0].value
    assert "STR" == result.children[1].type


def test_parses_string_operand_without_type(parser):
    result = parser("str_operand").parse('"String value"')

    assert "ESCAPED_STRING" == result.children[0].type
    assert '"String value"' == result.children[0].value


def test_parses_binding(parser):
    result = parser("binding").parse("identifier")

    assert "identifier" == result.children[0].value
    assert "CNAME" == result.children[0].type
