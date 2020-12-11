from lark import Transformer, v_args

from ..ast import (
    Constant,
    Instruction,
    Type,
    ASTRoot,
    ASTDefinition,
    ASTStruct,
    ASTFunction,
    ASTLabel,
    ASTNullaryInstruction,
    ASTUnaryInstruction,
    ASTOperand,
)


type_mapping = {
    "I8": Type.Int8,
    "I16": Type.Int16,
    "I32": Type.Int32,
    "I64": Type.Int64,
    "U8": Type.UInt8,
    "U16": Type.UInt16,
    "U32": Type.UInt32,
    "U64": Type.UInt64,
    "F32": Type.Float32,
    "F64": Type.Float64,
    "ADDR": Type.Address,
    "STR": Type.String,
}


instruction_mapping = {
    "HALT": Instruction.Halt,
    "NOOP": Instruction.Noop,
    "ADD": Instruction.Add,
    "SUB": Instruction.Sub,
    "MUL": Instruction.Mul,
    "DIV": Instruction.Div,
    "MOD": Instruction.Mod,
    "LDCONST": Instruction.LdConst,
    "LDLOCAL": Instruction.LdLocal,
    "STLOCAL": Instruction.StLocal,
    "POP": Instruction.Pop,
    "TESTEQ": Instruction.TestEQ,
    "TESTNE": Instruction.TestNE,
    "TESTLT": Instruction.TestLT,
    "TESTGT": Instruction.TestGT,
    "JMP": Instruction.Jmp,
    "JMPT": Instruction.JmpT,
    "JMPF": Instruction.JmpF,
    "CALLFUNC": Instruction.CallFunc,
    "CALLVIRT": Instruction.CallVirt,
    "RET": Instruction.Ret,
    "NEWSTRUCT": Instruction.NewStruct,
    "LDFIELD": Instruction.LdField,
    "STFIELD": Instruction.StField,
    "NEWARRAY": Instruction.NewArray,
    "LDELEM": Instruction.LdElem,
    "STELEM": Instruction.StElem,
}


@v_args(inline=True)
class ToAST(Transformer):
    @staticmethod
    def run_pass(tree):
        to_ast = ToAST()

        return to_ast.transform(tree)

    @v_args(inline=False)
    def start(self, children):
        return ASTRoot(children)

    def definition(self, name_token, operand):
        return ASTDefinition(
            name_token.value, operand, name_token.line, name_token.column
        )

    def struct(self, name_token, types):
        return ASTStruct(name_token.value, types, name_token.line, name_token.column)

    @v_args(inline=False)
    def types(self, tree):
        return [type_mapping[t.type] for t in tree]

    def function(self, name_token, locals_token, args_token, statements):
        symbol = name_token.value
        num_locals = int(locals_token.value)
        num_args = int(args_token.value)

        return ASTFunction(
            symbol, num_locals, num_args, statements, name_token.line, name_token.column
        )

    def statements(self, *stmts):
        return stmts

    def nullary_instruction(self, ins_token):
        instruction = instruction_mapping[ins_token.type]

        return ASTNullaryInstruction(instruction, ins_token.line, ins_token.column)

    def unary_instruction(self, ins_token, operand):
        instruction = instruction_mapping[ins_token.type]

        return ASTUnaryInstruction(
            instruction, operand, ins_token.line, ins_token.column
        )

    def label(self, token):
        symbol = token.value

        return ASTLabel(symbol, token.line, token.column)

    def int_operand(self, value, type_token=None):
        type_def = "I32"
        if type_token:
            type_def = type_token.type

        constant = Constant(type_mapping[type_def], int(value.value))

        return ASTOperand(constant, value.line, value.column)

    def float_operand(self, value, type_token):
        type_def = type_mapping[type_token.type]

        constant = Constant(type_def, float(value.value))

        return ASTOperand(constant, value.line, value.column)

    def str_operand(self, value, _=None):
        constant = Constant(Type.String, value.value)

        return ASTOperand(constant, value.line, value.column)

    def binding(self, token):
        return ASTOperand(token.value, token.line, token.column)
