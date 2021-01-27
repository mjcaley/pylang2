import binaryfile


def string(f: binaryfile.fileformat.BinarySectionBase):
    length = f.count("length", "string", 8)
    f.bytes("string", length)


def string_pool(f: binaryfile.fileformat.BinarySectionBase):
    f.array("strings")
    count = f.count("num_strings", "strings", 8)
    for i in range(count):
        f.section("strings", string)


def function(f: binaryfile.fileformat.BinarySectionBase):
    f.uint("name_index", 8)
    f.uint("locals", 8)
    f.uint("args", 8)
    f.uint("address", 8)


def function_pool(f: binaryfile.fileformat.BinarySectionBase):
    f.array("functions")
    count = f.count("num_functions", "functions", 8)
    for i in range(count):
        f.section("functions", function)


def file_spec(f: binaryfile.fileformat.BinarySectionBase):
    f.byteorder = "little"
    f.section("string_pool", string_pool)
    f.section("function_pool", function_pool)
    code_length = f.count("code_length", "code", 8)
    f.bytes("code", code_length)
