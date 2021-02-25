module.exports = grammar({
    name: 'pylang2',

    word: $ => $.identifier,

    rules: {
        start: $ => repeat(
            choice(
                $.definition,
                $.struct,
                $.function
            ),
        ),

        definition: $ => seq("define", $.identifier, $.type, "=", $._operand),

        struct: $ => seq(
            "struct",
            field("name", $.identifier),
            field("types", $._struct_types)
        ),
        _struct_types: $ => seq(
            $.type, repeat(seq(",", $.type))
        ),

        function: $ => seq(
            "func",
            field("name", $.identifier),
            "locals", "=",
            field("locals", $.dec_integer_literal),
            ",",
            "args", "=",
            field("args", $.dec_integer_literal),
            $.statements
        ),

        statements: $ => repeat1(
            choice($.instruction, $.label)
        ),
        instruction: $ => seq(
            choice($._nullary_instruction, $._unary_instruction),
            optional(seq($.type, $._operand))
        ),
        _nullary_instruction: $ => choice(
            "halt", "noop",
            "add", "sub", "mul", "div", "mod",
            "pop",
            "testeq", "testne", "testlt", "testgt",
            "callvirt",
            "ret"
        ),
        _unary_instruction: $ => choice(
            "ldconst",
            "ldlocal", "stlocal",
            "jmp", "jmpt", "jmpf",
            "callfunc",
            "newstruct", "ldfield", "stfield",
            "newarray", "ldelem", "stelem"
        ),
        label: $ => seq($.identifier, ":"),

        _operand: $ => choice($._literal, $.identifier),

        _literal: $ => seq(
            choice(
                $._number_literal,
                $.str_literal,
            )
        ),

        _number_literal: $ => seq(
            optional("-"),
            choice(
                $.bin_integer_literal,
                $.dec_integer_literal,
                $.hex_integer_literal,
                $.float_literal,
            )
        ),

        bin_integer_literal: $ => /0b[0-1]+/,
        dec_integer_literal: $ => /0|([1-9][0-9]+)/,
        hex_integer_literal: $ => /0x[0-9a-f]+/,
        _int_literal: $ => seq(
            choice($.bin_integer_literal, $.dec_integer_literal, $.hex_integer_literal)
        ),
        float_literal: $ => /(0|([1-9][0-9]))+\.[0-9]+/,
        str_literal: $ => seq('"', /[^\n\r\f"]*/, '"'),

        type: $ => choice(
            "i8", "i16", "i32", "i64",
            "u8", "u16", "u32", "u64",
            "f32", "f64",
            "str",
            "void"
        ),

        identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,

        _newline: $ => /\n|\r\n/,
    }
});
