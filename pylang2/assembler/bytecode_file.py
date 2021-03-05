from construct import Array, Bytes, Const, Struct, Int64ul, Int16ul, Rebuild, len_, this


FileFormat = Struct(
    Const(b"pylang2"),
    "version" / Int16ul,
    # String pool
    "string_count" / Rebuild(Int64ul, len_(this.strings)),
    "strings"
    / Array(
        this.string_count,
        Struct(
            "length" / Rebuild(Int64ul, len_(this.string)),
            "string" / Bytes(this.length),
        ),
    ),
    # Function pool
    "function_count" / Rebuild(Int64ul, len_(this.functions)),
    "functions"
    / Array(
        this.function_count,
        Struct(
            "name_index" / Int64ul,
            "locals" / Int64ul,
            "args" / Int64ul,
            "address" / Int64ul,
        ),
    ),
    "code_length" / Rebuild(Int64ul, len_(this.code)),
    "code" / Bytes(this.code_length),
)
