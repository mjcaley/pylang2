#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 12
#define STATE_COUNT 42
#define LARGE_STATE_COUNT 3
#define SYMBOL_COUNT 74
#define ALIAS_COUNT 0
#define TOKEN_COUNT 56
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 4
#define MAX_ALIAS_SEQUENCE_LENGTH 10

enum {
  sym_identifier = 1,
  anon_sym_define = 2,
  anon_sym_EQ = 3,
  anon_sym_struct = 4,
  anon_sym_COMMA = 5,
  anon_sym_func = 6,
  anon_sym_locals = 7,
  anon_sym_args = 8,
  anon_sym_halt = 9,
  anon_sym_noop = 10,
  anon_sym_add = 11,
  anon_sym_sub = 12,
  anon_sym_mul = 13,
  anon_sym_div = 14,
  anon_sym_mod = 15,
  anon_sym_pop = 16,
  anon_sym_testeq = 17,
  anon_sym_testne = 18,
  anon_sym_testlt = 19,
  anon_sym_testgt = 20,
  anon_sym_callvirt = 21,
  anon_sym_ret = 22,
  anon_sym_ldconst = 23,
  anon_sym_ldlocal = 24,
  anon_sym_stlocal = 25,
  anon_sym_jmp = 26,
  anon_sym_jmpt = 27,
  anon_sym_jmpf = 28,
  anon_sym_callfunc = 29,
  anon_sym_newstruct = 30,
  anon_sym_ldfield = 31,
  anon_sym_stfield = 32,
  anon_sym_newarray = 33,
  anon_sym_ldelem = 34,
  anon_sym_stelem = 35,
  anon_sym_COLON = 36,
  anon_sym_DASH = 37,
  sym_bin_integer_literal = 38,
  sym_dec_integer_literal = 39,
  sym_hex_integer_literal = 40,
  sym_float_literal = 41,
  anon_sym_DQUOTE = 42,
  aux_sym_str_literal_token1 = 43,
  anon_sym_i8 = 44,
  anon_sym_i16 = 45,
  anon_sym_i32 = 46,
  anon_sym_i64 = 47,
  anon_sym_u8 = 48,
  anon_sym_u16 = 49,
  anon_sym_u32 = 50,
  anon_sym_u64 = 51,
  anon_sym_f32 = 52,
  anon_sym_f64 = 53,
  anon_sym_str = 54,
  anon_sym_void = 55,
  sym_start = 56,
  sym_definition = 57,
  sym_struct = 58,
  sym__struct_types = 59,
  sym_function = 60,
  sym_statements = 61,
  sym_instruction = 62,
  sym__nullary_instruction = 63,
  sym__unary_instruction = 64,
  sym_label = 65,
  sym__operand = 66,
  sym__literal = 67,
  sym__number_literal = 68,
  sym_str_literal = 69,
  sym_type = 70,
  aux_sym_start_repeat1 = 71,
  aux_sym__struct_types_repeat1 = 72,
  aux_sym_statements_repeat1 = 73,
};

static const char *ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_identifier] = "identifier",
  [anon_sym_define] = "define",
  [anon_sym_EQ] = "=",
  [anon_sym_struct] = "struct",
  [anon_sym_COMMA] = ",",
  [anon_sym_func] = "func",
  [anon_sym_locals] = "locals",
  [anon_sym_args] = "args",
  [anon_sym_halt] = "halt",
  [anon_sym_noop] = "noop",
  [anon_sym_add] = "add",
  [anon_sym_sub] = "sub",
  [anon_sym_mul] = "mul",
  [anon_sym_div] = "div",
  [anon_sym_mod] = "mod",
  [anon_sym_pop] = "pop",
  [anon_sym_testeq] = "testeq",
  [anon_sym_testne] = "testne",
  [anon_sym_testlt] = "testlt",
  [anon_sym_testgt] = "testgt",
  [anon_sym_callvirt] = "callvirt",
  [anon_sym_ret] = "ret",
  [anon_sym_ldconst] = "ldconst",
  [anon_sym_ldlocal] = "ldlocal",
  [anon_sym_stlocal] = "stlocal",
  [anon_sym_jmp] = "jmp",
  [anon_sym_jmpt] = "jmpt",
  [anon_sym_jmpf] = "jmpf",
  [anon_sym_callfunc] = "callfunc",
  [anon_sym_newstruct] = "newstruct",
  [anon_sym_ldfield] = "ldfield",
  [anon_sym_stfield] = "stfield",
  [anon_sym_newarray] = "newarray",
  [anon_sym_ldelem] = "ldelem",
  [anon_sym_stelem] = "stelem",
  [anon_sym_COLON] = ":",
  [anon_sym_DASH] = "-",
  [sym_bin_integer_literal] = "bin_integer_literal",
  [sym_dec_integer_literal] = "dec_integer_literal",
  [sym_hex_integer_literal] = "hex_integer_literal",
  [sym_float_literal] = "float_literal",
  [anon_sym_DQUOTE] = "\"",
  [aux_sym_str_literal_token1] = "str_literal_token1",
  [anon_sym_i8] = "i8",
  [anon_sym_i16] = "i16",
  [anon_sym_i32] = "i32",
  [anon_sym_i64] = "i64",
  [anon_sym_u8] = "u8",
  [anon_sym_u16] = "u16",
  [anon_sym_u32] = "u32",
  [anon_sym_u64] = "u64",
  [anon_sym_f32] = "f32",
  [anon_sym_f64] = "f64",
  [anon_sym_str] = "str",
  [anon_sym_void] = "void",
  [sym_start] = "start",
  [sym_definition] = "definition",
  [sym_struct] = "struct",
  [sym__struct_types] = "_struct_types",
  [sym_function] = "function",
  [sym_statements] = "statements",
  [sym_instruction] = "instruction",
  [sym__nullary_instruction] = "_nullary_instruction",
  [sym__unary_instruction] = "_unary_instruction",
  [sym_label] = "label",
  [sym__operand] = "_operand",
  [sym__literal] = "_literal",
  [sym__number_literal] = "_number_literal",
  [sym_str_literal] = "str_literal",
  [sym_type] = "type",
  [aux_sym_start_repeat1] = "start_repeat1",
  [aux_sym__struct_types_repeat1] = "_struct_types_repeat1",
  [aux_sym_statements_repeat1] = "statements_repeat1",
};

static TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_identifier] = sym_identifier,
  [anon_sym_define] = anon_sym_define,
  [anon_sym_EQ] = anon_sym_EQ,
  [anon_sym_struct] = anon_sym_struct,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [anon_sym_func] = anon_sym_func,
  [anon_sym_locals] = anon_sym_locals,
  [anon_sym_args] = anon_sym_args,
  [anon_sym_halt] = anon_sym_halt,
  [anon_sym_noop] = anon_sym_noop,
  [anon_sym_add] = anon_sym_add,
  [anon_sym_sub] = anon_sym_sub,
  [anon_sym_mul] = anon_sym_mul,
  [anon_sym_div] = anon_sym_div,
  [anon_sym_mod] = anon_sym_mod,
  [anon_sym_pop] = anon_sym_pop,
  [anon_sym_testeq] = anon_sym_testeq,
  [anon_sym_testne] = anon_sym_testne,
  [anon_sym_testlt] = anon_sym_testlt,
  [anon_sym_testgt] = anon_sym_testgt,
  [anon_sym_callvirt] = anon_sym_callvirt,
  [anon_sym_ret] = anon_sym_ret,
  [anon_sym_ldconst] = anon_sym_ldconst,
  [anon_sym_ldlocal] = anon_sym_ldlocal,
  [anon_sym_stlocal] = anon_sym_stlocal,
  [anon_sym_jmp] = anon_sym_jmp,
  [anon_sym_jmpt] = anon_sym_jmpt,
  [anon_sym_jmpf] = anon_sym_jmpf,
  [anon_sym_callfunc] = anon_sym_callfunc,
  [anon_sym_newstruct] = anon_sym_newstruct,
  [anon_sym_ldfield] = anon_sym_ldfield,
  [anon_sym_stfield] = anon_sym_stfield,
  [anon_sym_newarray] = anon_sym_newarray,
  [anon_sym_ldelem] = anon_sym_ldelem,
  [anon_sym_stelem] = anon_sym_stelem,
  [anon_sym_COLON] = anon_sym_COLON,
  [anon_sym_DASH] = anon_sym_DASH,
  [sym_bin_integer_literal] = sym_bin_integer_literal,
  [sym_dec_integer_literal] = sym_dec_integer_literal,
  [sym_hex_integer_literal] = sym_hex_integer_literal,
  [sym_float_literal] = sym_float_literal,
  [anon_sym_DQUOTE] = anon_sym_DQUOTE,
  [aux_sym_str_literal_token1] = aux_sym_str_literal_token1,
  [anon_sym_i8] = anon_sym_i8,
  [anon_sym_i16] = anon_sym_i16,
  [anon_sym_i32] = anon_sym_i32,
  [anon_sym_i64] = anon_sym_i64,
  [anon_sym_u8] = anon_sym_u8,
  [anon_sym_u16] = anon_sym_u16,
  [anon_sym_u32] = anon_sym_u32,
  [anon_sym_u64] = anon_sym_u64,
  [anon_sym_f32] = anon_sym_f32,
  [anon_sym_f64] = anon_sym_f64,
  [anon_sym_str] = anon_sym_str,
  [anon_sym_void] = anon_sym_void,
  [sym_start] = sym_start,
  [sym_definition] = sym_definition,
  [sym_struct] = sym_struct,
  [sym__struct_types] = sym__struct_types,
  [sym_function] = sym_function,
  [sym_statements] = sym_statements,
  [sym_instruction] = sym_instruction,
  [sym__nullary_instruction] = sym__nullary_instruction,
  [sym__unary_instruction] = sym__unary_instruction,
  [sym_label] = sym_label,
  [sym__operand] = sym__operand,
  [sym__literal] = sym__literal,
  [sym__number_literal] = sym__number_literal,
  [sym_str_literal] = sym_str_literal,
  [sym_type] = sym_type,
  [aux_sym_start_repeat1] = aux_sym_start_repeat1,
  [aux_sym__struct_types_repeat1] = aux_sym__struct_types_repeat1,
  [aux_sym_statements_repeat1] = aux_sym_statements_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_define] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_struct] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_func] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_locals] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_args] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_halt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_noop] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_add] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_sub] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_mul] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_div] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_mod] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_pop] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_testeq] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_testne] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_testlt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_testgt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_callvirt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ret] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ldconst] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ldlocal] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_stlocal] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_jmp] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_jmpt] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_jmpf] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_callfunc] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_newstruct] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ldfield] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_stfield] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_newarray] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ldelem] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_stelem] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH] = {
    .visible = true,
    .named = false,
  },
  [sym_bin_integer_literal] = {
    .visible = true,
    .named = true,
  },
  [sym_dec_integer_literal] = {
    .visible = true,
    .named = true,
  },
  [sym_hex_integer_literal] = {
    .visible = true,
    .named = true,
  },
  [sym_float_literal] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_DQUOTE] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_str_literal_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_i8] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i16] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i32] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_i64] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u8] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u16] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u32] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u64] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_f32] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_f64] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_str] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_void] = {
    .visible = true,
    .named = false,
  },
  [sym_start] = {
    .visible = true,
    .named = true,
  },
  [sym_definition] = {
    .visible = true,
    .named = true,
  },
  [sym_struct] = {
    .visible = true,
    .named = true,
  },
  [sym__struct_types] = {
    .visible = false,
    .named = true,
  },
  [sym_function] = {
    .visible = true,
    .named = true,
  },
  [sym_statements] = {
    .visible = true,
    .named = true,
  },
  [sym_instruction] = {
    .visible = true,
    .named = true,
  },
  [sym__nullary_instruction] = {
    .visible = false,
    .named = true,
  },
  [sym__unary_instruction] = {
    .visible = false,
    .named = true,
  },
  [sym_label] = {
    .visible = true,
    .named = true,
  },
  [sym__operand] = {
    .visible = false,
    .named = true,
  },
  [sym__literal] = {
    .visible = false,
    .named = true,
  },
  [sym__number_literal] = {
    .visible = false,
    .named = true,
  },
  [sym_str_literal] = {
    .visible = true,
    .named = true,
  },
  [sym_type] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_start_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym__struct_types_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_statements_repeat1] = {
    .visible = false,
    .named = false,
  },
};

enum {
  field_args = 1,
  field_locals = 2,
  field_name = 3,
  field_types = 4,
};

static const char *ts_field_names[] = {
  [0] = NULL,
  [field_args] = "args",
  [field_locals] = "locals",
  [field_name] = "name",
  [field_types] = "types",
};

static const TSFieldMapSlice ts_field_map_slices[3] = {
  [1] = {.index = 0, .length = 2},
  [2] = {.index = 2, .length = 3},
};

static const TSFieldMapEntry ts_field_map_entries[] = {
  [0] =
    {field_name, 1},
    {field_types, 2},
  [2] =
    {field_args, 8},
    {field_locals, 4},
    {field_name, 1},
};

static TSSymbol ts_alias_sequences[3][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(9);
      if (lookahead == '"') ADVANCE(22);
      if (lookahead == ',') ADVANCE(11);
      if (lookahead == '-') ADVANCE(13);
      if (lookahead == '0') ADVANCE(16);
      if (lookahead == ':') ADVANCE(12);
      if (lookahead == '=') ADVANCE(10);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(5);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(25);
      END_STATE();
    case 1:
      if (lookahead == '.') ADVANCE(6);
      if (lookahead == '0') ADVANCE(1);
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(4);
      END_STATE();
    case 2:
      if (lookahead == '0') ADVANCE(15);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(2)
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(7);
      END_STATE();
    case 3:
      if (lookahead == '0' ||
          lookahead == '1') ADVANCE(14);
      END_STATE();
    case 4:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(1);
      END_STATE();
    case 5:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      END_STATE();
    case 6:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(21);
      END_STATE();
    case 7:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      END_STATE();
    case 8:
      if (('0' <= lookahead && lookahead <= '9') ||
          ('a' <= lookahead && lookahead <= 'f')) ADVANCE(20);
      END_STATE();
    case 9:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 10:
      ACCEPT_TOKEN(anon_sym_EQ);
      END_STATE();
    case 11:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 12:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 13:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 14:
      ACCEPT_TOKEN(sym_bin_integer_literal);
      if (lookahead == '0' ||
          lookahead == '1') ADVANCE(14);
      END_STATE();
    case 15:
      ACCEPT_TOKEN(sym_dec_integer_literal);
      END_STATE();
    case 16:
      ACCEPT_TOKEN(sym_dec_integer_literal);
      if (lookahead == '.') ADVANCE(6);
      if (lookahead == '0') ADVANCE(1);
      if (lookahead == 'b') ADVANCE(3);
      if (lookahead == 'x') ADVANCE(8);
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(4);
      END_STATE();
    case 17:
      ACCEPT_TOKEN(sym_dec_integer_literal);
      if (lookahead == '.') ADVANCE(6);
      if (lookahead == '0') ADVANCE(17);
      if (('1' <= lookahead && lookahead <= '9')) ADVANCE(18);
      END_STATE();
    case 18:
      ACCEPT_TOKEN(sym_dec_integer_literal);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      END_STATE();
    case 19:
      ACCEPT_TOKEN(sym_dec_integer_literal);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      END_STATE();
    case 20:
      ACCEPT_TOKEN(sym_hex_integer_literal);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('a' <= lookahead && lookahead <= 'f')) ADVANCE(20);
      END_STATE();
    case 21:
      ACCEPT_TOKEN(sym_float_literal);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(21);
      END_STATE();
    case 22:
      ACCEPT_TOKEN(anon_sym_DQUOTE);
      END_STATE();
    case 23:
      ACCEPT_TOKEN(aux_sym_str_literal_token1);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(23);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '\f' &&
          lookahead != '\r' &&
          lookahead != '"') ADVANCE(24);
      END_STATE();
    case 24:
      ACCEPT_TOKEN(aux_sym_str_literal_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '\f' &&
          lookahead != '\r' &&
          lookahead != '"') ADVANCE(24);
      END_STATE();
    case 25:
      ACCEPT_TOKEN(sym_identifier);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(25);
      END_STATE();
    default:
      return false;
  }
}

static bool ts_lex_keywords(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (lookahead == 'a') ADVANCE(1);
      if (lookahead == 'c') ADVANCE(2);
      if (lookahead == 'd') ADVANCE(3);
      if (lookahead == 'f') ADVANCE(4);
      if (lookahead == 'h') ADVANCE(5);
      if (lookahead == 'i') ADVANCE(6);
      if (lookahead == 'j') ADVANCE(7);
      if (lookahead == 'l') ADVANCE(8);
      if (lookahead == 'm') ADVANCE(9);
      if (lookahead == 'n') ADVANCE(10);
      if (lookahead == 'p') ADVANCE(11);
      if (lookahead == 'r') ADVANCE(12);
      if (lookahead == 's') ADVANCE(13);
      if (lookahead == 't') ADVANCE(14);
      if (lookahead == 'u') ADVANCE(15);
      if (lookahead == 'v') ADVANCE(16);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      END_STATE();
    case 1:
      if (lookahead == 'd') ADVANCE(17);
      if (lookahead == 'r') ADVANCE(18);
      END_STATE();
    case 2:
      if (lookahead == 'a') ADVANCE(19);
      END_STATE();
    case 3:
      if (lookahead == 'e') ADVANCE(20);
      if (lookahead == 'i') ADVANCE(21);
      END_STATE();
    case 4:
      if (lookahead == '3') ADVANCE(22);
      if (lookahead == '6') ADVANCE(23);
      if (lookahead == 'u') ADVANCE(24);
      END_STATE();
    case 5:
      if (lookahead == 'a') ADVANCE(25);
      END_STATE();
    case 6:
      if (lookahead == '1') ADVANCE(26);
      if (lookahead == '3') ADVANCE(27);
      if (lookahead == '6') ADVANCE(28);
      if (lookahead == '8') ADVANCE(29);
      END_STATE();
    case 7:
      if (lookahead == 'm') ADVANCE(30);
      END_STATE();
    case 8:
      if (lookahead == 'd') ADVANCE(31);
      if (lookahead == 'o') ADVANCE(32);
      END_STATE();
    case 9:
      if (lookahead == 'o') ADVANCE(33);
      if (lookahead == 'u') ADVANCE(34);
      END_STATE();
    case 10:
      if (lookahead == 'e') ADVANCE(35);
      if (lookahead == 'o') ADVANCE(36);
      END_STATE();
    case 11:
      if (lookahead == 'o') ADVANCE(37);
      END_STATE();
    case 12:
      if (lookahead == 'e') ADVANCE(38);
      END_STATE();
    case 13:
      if (lookahead == 't') ADVANCE(39);
      if (lookahead == 'u') ADVANCE(40);
      END_STATE();
    case 14:
      if (lookahead == 'e') ADVANCE(41);
      END_STATE();
    case 15:
      if (lookahead == '1') ADVANCE(42);
      if (lookahead == '3') ADVANCE(43);
      if (lookahead == '6') ADVANCE(44);
      if (lookahead == '8') ADVANCE(45);
      END_STATE();
    case 16:
      if (lookahead == 'o') ADVANCE(46);
      END_STATE();
    case 17:
      if (lookahead == 'd') ADVANCE(47);
      END_STATE();
    case 18:
      if (lookahead == 'g') ADVANCE(48);
      END_STATE();
    case 19:
      if (lookahead == 'l') ADVANCE(49);
      END_STATE();
    case 20:
      if (lookahead == 'f') ADVANCE(50);
      END_STATE();
    case 21:
      if (lookahead == 'v') ADVANCE(51);
      END_STATE();
    case 22:
      if (lookahead == '2') ADVANCE(52);
      END_STATE();
    case 23:
      if (lookahead == '4') ADVANCE(53);
      END_STATE();
    case 24:
      if (lookahead == 'n') ADVANCE(54);
      END_STATE();
    case 25:
      if (lookahead == 'l') ADVANCE(55);
      END_STATE();
    case 26:
      if (lookahead == '6') ADVANCE(56);
      END_STATE();
    case 27:
      if (lookahead == '2') ADVANCE(57);
      END_STATE();
    case 28:
      if (lookahead == '4') ADVANCE(58);
      END_STATE();
    case 29:
      ACCEPT_TOKEN(anon_sym_i8);
      END_STATE();
    case 30:
      if (lookahead == 'p') ADVANCE(59);
      END_STATE();
    case 31:
      if (lookahead == 'c') ADVANCE(60);
      if (lookahead == 'e') ADVANCE(61);
      if (lookahead == 'f') ADVANCE(62);
      if (lookahead == 'l') ADVANCE(63);
      END_STATE();
    case 32:
      if (lookahead == 'c') ADVANCE(64);
      END_STATE();
    case 33:
      if (lookahead == 'd') ADVANCE(65);
      END_STATE();
    case 34:
      if (lookahead == 'l') ADVANCE(66);
      END_STATE();
    case 35:
      if (lookahead == 'w') ADVANCE(67);
      END_STATE();
    case 36:
      if (lookahead == 'o') ADVANCE(68);
      END_STATE();
    case 37:
      if (lookahead == 'p') ADVANCE(69);
      END_STATE();
    case 38:
      if (lookahead == 't') ADVANCE(70);
      END_STATE();
    case 39:
      if (lookahead == 'e') ADVANCE(71);
      if (lookahead == 'f') ADVANCE(72);
      if (lookahead == 'l') ADVANCE(73);
      if (lookahead == 'r') ADVANCE(74);
      END_STATE();
    case 40:
      if (lookahead == 'b') ADVANCE(75);
      END_STATE();
    case 41:
      if (lookahead == 's') ADVANCE(76);
      END_STATE();
    case 42:
      if (lookahead == '6') ADVANCE(77);
      END_STATE();
    case 43:
      if (lookahead == '2') ADVANCE(78);
      END_STATE();
    case 44:
      if (lookahead == '4') ADVANCE(79);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(anon_sym_u8);
      END_STATE();
    case 46:
      if (lookahead == 'i') ADVANCE(80);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(anon_sym_add);
      END_STATE();
    case 48:
      if (lookahead == 's') ADVANCE(81);
      END_STATE();
    case 49:
      if (lookahead == 'l') ADVANCE(82);
      END_STATE();
    case 50:
      if (lookahead == 'i') ADVANCE(83);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(anon_sym_div);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(anon_sym_f32);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(anon_sym_f64);
      END_STATE();
    case 54:
      if (lookahead == 'c') ADVANCE(84);
      END_STATE();
    case 55:
      if (lookahead == 't') ADVANCE(85);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(anon_sym_i16);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(anon_sym_i32);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(anon_sym_i64);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(anon_sym_jmp);
      if (lookahead == 'f') ADVANCE(86);
      if (lookahead == 't') ADVANCE(87);
      END_STATE();
    case 60:
      if (lookahead == 'o') ADVANCE(88);
      END_STATE();
    case 61:
      if (lookahead == 'l') ADVANCE(89);
      END_STATE();
    case 62:
      if (lookahead == 'i') ADVANCE(90);
      END_STATE();
    case 63:
      if (lookahead == 'o') ADVANCE(91);
      END_STATE();
    case 64:
      if (lookahead == 'a') ADVANCE(92);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(anon_sym_mod);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(anon_sym_mul);
      END_STATE();
    case 67:
      if (lookahead == 'a') ADVANCE(93);
      if (lookahead == 's') ADVANCE(94);
      END_STATE();
    case 68:
      if (lookahead == 'p') ADVANCE(95);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(anon_sym_pop);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(anon_sym_ret);
      END_STATE();
    case 71:
      if (lookahead == 'l') ADVANCE(96);
      END_STATE();
    case 72:
      if (lookahead == 'i') ADVANCE(97);
      END_STATE();
    case 73:
      if (lookahead == 'o') ADVANCE(98);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(anon_sym_str);
      if (lookahead == 'u') ADVANCE(99);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(anon_sym_sub);
      END_STATE();
    case 76:
      if (lookahead == 't') ADVANCE(100);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(anon_sym_u16);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(anon_sym_u32);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(anon_sym_u64);
      END_STATE();
    case 80:
      if (lookahead == 'd') ADVANCE(101);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(anon_sym_args);
      END_STATE();
    case 82:
      if (lookahead == 'f') ADVANCE(102);
      if (lookahead == 'v') ADVANCE(103);
      END_STATE();
    case 83:
      if (lookahead == 'n') ADVANCE(104);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(anon_sym_func);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(anon_sym_halt);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(anon_sym_jmpf);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(anon_sym_jmpt);
      END_STATE();
    case 88:
      if (lookahead == 'n') ADVANCE(105);
      END_STATE();
    case 89:
      if (lookahead == 'e') ADVANCE(106);
      END_STATE();
    case 90:
      if (lookahead == 'e') ADVANCE(107);
      END_STATE();
    case 91:
      if (lookahead == 'c') ADVANCE(108);
      END_STATE();
    case 92:
      if (lookahead == 'l') ADVANCE(109);
      END_STATE();
    case 93:
      if (lookahead == 'r') ADVANCE(110);
      END_STATE();
    case 94:
      if (lookahead == 't') ADVANCE(111);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(anon_sym_noop);
      END_STATE();
    case 96:
      if (lookahead == 'e') ADVANCE(112);
      END_STATE();
    case 97:
      if (lookahead == 'e') ADVANCE(113);
      END_STATE();
    case 98:
      if (lookahead == 'c') ADVANCE(114);
      END_STATE();
    case 99:
      if (lookahead == 'c') ADVANCE(115);
      END_STATE();
    case 100:
      if (lookahead == 'e') ADVANCE(116);
      if (lookahead == 'g') ADVANCE(117);
      if (lookahead == 'l') ADVANCE(118);
      if (lookahead == 'n') ADVANCE(119);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(anon_sym_void);
      END_STATE();
    case 102:
      if (lookahead == 'u') ADVANCE(120);
      END_STATE();
    case 103:
      if (lookahead == 'i') ADVANCE(121);
      END_STATE();
    case 104:
      if (lookahead == 'e') ADVANCE(122);
      END_STATE();
    case 105:
      if (lookahead == 's') ADVANCE(123);
      END_STATE();
    case 106:
      if (lookahead == 'm') ADVANCE(124);
      END_STATE();
    case 107:
      if (lookahead == 'l') ADVANCE(125);
      END_STATE();
    case 108:
      if (lookahead == 'a') ADVANCE(126);
      END_STATE();
    case 109:
      if (lookahead == 's') ADVANCE(127);
      END_STATE();
    case 110:
      if (lookahead == 'r') ADVANCE(128);
      END_STATE();
    case 111:
      if (lookahead == 'r') ADVANCE(129);
      END_STATE();
    case 112:
      if (lookahead == 'm') ADVANCE(130);
      END_STATE();
    case 113:
      if (lookahead == 'l') ADVANCE(131);
      END_STATE();
    case 114:
      if (lookahead == 'a') ADVANCE(132);
      END_STATE();
    case 115:
      if (lookahead == 't') ADVANCE(133);
      END_STATE();
    case 116:
      if (lookahead == 'q') ADVANCE(134);
      END_STATE();
    case 117:
      if (lookahead == 't') ADVANCE(135);
      END_STATE();
    case 118:
      if (lookahead == 't') ADVANCE(136);
      END_STATE();
    case 119:
      if (lookahead == 'e') ADVANCE(137);
      END_STATE();
    case 120:
      if (lookahead == 'n') ADVANCE(138);
      END_STATE();
    case 121:
      if (lookahead == 'r') ADVANCE(139);
      END_STATE();
    case 122:
      ACCEPT_TOKEN(anon_sym_define);
      END_STATE();
    case 123:
      if (lookahead == 't') ADVANCE(140);
      END_STATE();
    case 124:
      ACCEPT_TOKEN(anon_sym_ldelem);
      END_STATE();
    case 125:
      if (lookahead == 'd') ADVANCE(141);
      END_STATE();
    case 126:
      if (lookahead == 'l') ADVANCE(142);
      END_STATE();
    case 127:
      ACCEPT_TOKEN(anon_sym_locals);
      END_STATE();
    case 128:
      if (lookahead == 'a') ADVANCE(143);
      END_STATE();
    case 129:
      if (lookahead == 'u') ADVANCE(144);
      END_STATE();
    case 130:
      ACCEPT_TOKEN(anon_sym_stelem);
      END_STATE();
    case 131:
      if (lookahead == 'd') ADVANCE(145);
      END_STATE();
    case 132:
      if (lookahead == 'l') ADVANCE(146);
      END_STATE();
    case 133:
      ACCEPT_TOKEN(anon_sym_struct);
      END_STATE();
    case 134:
      ACCEPT_TOKEN(anon_sym_testeq);
      END_STATE();
    case 135:
      ACCEPT_TOKEN(anon_sym_testgt);
      END_STATE();
    case 136:
      ACCEPT_TOKEN(anon_sym_testlt);
      END_STATE();
    case 137:
      ACCEPT_TOKEN(anon_sym_testne);
      END_STATE();
    case 138:
      if (lookahead == 'c') ADVANCE(147);
      END_STATE();
    case 139:
      if (lookahead == 't') ADVANCE(148);
      END_STATE();
    case 140:
      ACCEPT_TOKEN(anon_sym_ldconst);
      END_STATE();
    case 141:
      ACCEPT_TOKEN(anon_sym_ldfield);
      END_STATE();
    case 142:
      ACCEPT_TOKEN(anon_sym_ldlocal);
      END_STATE();
    case 143:
      if (lookahead == 'y') ADVANCE(149);
      END_STATE();
    case 144:
      if (lookahead == 'c') ADVANCE(150);
      END_STATE();
    case 145:
      ACCEPT_TOKEN(anon_sym_stfield);
      END_STATE();
    case 146:
      ACCEPT_TOKEN(anon_sym_stlocal);
      END_STATE();
    case 147:
      ACCEPT_TOKEN(anon_sym_callfunc);
      END_STATE();
    case 148:
      ACCEPT_TOKEN(anon_sym_callvirt);
      END_STATE();
    case 149:
      ACCEPT_TOKEN(anon_sym_newarray);
      END_STATE();
    case 150:
      if (lookahead == 't') ADVANCE(151);
      END_STATE();
    case 151:
      ACCEPT_TOKEN(anon_sym_newstruct);
      END_STATE();
    default:
      return false;
  }
}

static TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 0},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 0},
  [4] = {.lex_state = 0},
  [5] = {.lex_state = 0},
  [6] = {.lex_state = 0},
  [7] = {.lex_state = 0},
  [8] = {.lex_state = 0},
  [9] = {.lex_state = 0},
  [10] = {.lex_state = 0},
  [11] = {.lex_state = 0},
  [12] = {.lex_state = 0},
  [13] = {.lex_state = 0},
  [14] = {.lex_state = 0},
  [15] = {.lex_state = 0},
  [16] = {.lex_state = 0},
  [17] = {.lex_state = 0},
  [18] = {.lex_state = 0},
  [19] = {.lex_state = 0},
  [20] = {.lex_state = 0},
  [21] = {.lex_state = 0},
  [22] = {.lex_state = 0},
  [23] = {.lex_state = 0},
  [24] = {.lex_state = 0},
  [25] = {.lex_state = 0},
  [26] = {.lex_state = 0},
  [27] = {.lex_state = 0},
  [28] = {.lex_state = 0},
  [29] = {.lex_state = 0},
  [30] = {.lex_state = 0},
  [31] = {.lex_state = 23},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 2},
  [34] = {.lex_state = 2},
  [35] = {.lex_state = 0},
  [36] = {.lex_state = 0},
  [37] = {.lex_state = 0},
  [38] = {.lex_state = 0},
  [39] = {.lex_state = 0},
  [40] = {.lex_state = 0},
  [41] = {.lex_state = 0},
};

static uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_identifier] = ACTIONS(1),
    [anon_sym_define] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [anon_sym_struct] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [anon_sym_func] = ACTIONS(1),
    [anon_sym_locals] = ACTIONS(1),
    [anon_sym_args] = ACTIONS(1),
    [anon_sym_halt] = ACTIONS(1),
    [anon_sym_noop] = ACTIONS(1),
    [anon_sym_add] = ACTIONS(1),
    [anon_sym_sub] = ACTIONS(1),
    [anon_sym_mul] = ACTIONS(1),
    [anon_sym_div] = ACTIONS(1),
    [anon_sym_mod] = ACTIONS(1),
    [anon_sym_pop] = ACTIONS(1),
    [anon_sym_testeq] = ACTIONS(1),
    [anon_sym_testne] = ACTIONS(1),
    [anon_sym_testlt] = ACTIONS(1),
    [anon_sym_testgt] = ACTIONS(1),
    [anon_sym_callvirt] = ACTIONS(1),
    [anon_sym_ret] = ACTIONS(1),
    [anon_sym_ldconst] = ACTIONS(1),
    [anon_sym_ldlocal] = ACTIONS(1),
    [anon_sym_stlocal] = ACTIONS(1),
    [anon_sym_jmp] = ACTIONS(1),
    [anon_sym_jmpt] = ACTIONS(1),
    [anon_sym_jmpf] = ACTIONS(1),
    [anon_sym_callfunc] = ACTIONS(1),
    [anon_sym_newstruct] = ACTIONS(1),
    [anon_sym_ldfield] = ACTIONS(1),
    [anon_sym_stfield] = ACTIONS(1),
    [anon_sym_newarray] = ACTIONS(1),
    [anon_sym_ldelem] = ACTIONS(1),
    [anon_sym_stelem] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
    [anon_sym_DASH] = ACTIONS(1),
    [sym_bin_integer_literal] = ACTIONS(1),
    [sym_dec_integer_literal] = ACTIONS(1),
    [sym_hex_integer_literal] = ACTIONS(1),
    [sym_float_literal] = ACTIONS(1),
    [anon_sym_DQUOTE] = ACTIONS(1),
    [anon_sym_i8] = ACTIONS(1),
    [anon_sym_i16] = ACTIONS(1),
    [anon_sym_i32] = ACTIONS(1),
    [anon_sym_i64] = ACTIONS(1),
    [anon_sym_u8] = ACTIONS(1),
    [anon_sym_u16] = ACTIONS(1),
    [anon_sym_u32] = ACTIONS(1),
    [anon_sym_u64] = ACTIONS(1),
    [anon_sym_f32] = ACTIONS(1),
    [anon_sym_f64] = ACTIONS(1),
    [anon_sym_str] = ACTIONS(1),
    [anon_sym_void] = ACTIONS(1),
  },
  [1] = {
    [sym_start] = STATE(39),
    [sym_definition] = STATE(16),
    [sym_struct] = STATE(16),
    [sym_function] = STATE(16),
    [aux_sym_start_repeat1] = STATE(16),
    [ts_builtin_sym_end] = ACTIONS(3),
    [anon_sym_define] = ACTIONS(5),
    [anon_sym_struct] = ACTIONS(7),
    [anon_sym_func] = ACTIONS(9),
  },
  [2] = {
    [sym_type] = STATE(13),
    [ts_builtin_sym_end] = ACTIONS(11),
    [sym_identifier] = ACTIONS(13),
    [anon_sym_define] = ACTIONS(13),
    [anon_sym_struct] = ACTIONS(13),
    [anon_sym_func] = ACTIONS(13),
    [anon_sym_halt] = ACTIONS(13),
    [anon_sym_noop] = ACTIONS(13),
    [anon_sym_add] = ACTIONS(13),
    [anon_sym_sub] = ACTIONS(13),
    [anon_sym_mul] = ACTIONS(13),
    [anon_sym_div] = ACTIONS(13),
    [anon_sym_mod] = ACTIONS(13),
    [anon_sym_pop] = ACTIONS(13),
    [anon_sym_testeq] = ACTIONS(13),
    [anon_sym_testne] = ACTIONS(13),
    [anon_sym_testlt] = ACTIONS(13),
    [anon_sym_testgt] = ACTIONS(13),
    [anon_sym_callvirt] = ACTIONS(13),
    [anon_sym_ret] = ACTIONS(13),
    [anon_sym_ldconst] = ACTIONS(13),
    [anon_sym_ldlocal] = ACTIONS(13),
    [anon_sym_stlocal] = ACTIONS(13),
    [anon_sym_jmp] = ACTIONS(13),
    [anon_sym_jmpt] = ACTIONS(13),
    [anon_sym_jmpf] = ACTIONS(13),
    [anon_sym_callfunc] = ACTIONS(13),
    [anon_sym_newstruct] = ACTIONS(13),
    [anon_sym_ldfield] = ACTIONS(13),
    [anon_sym_stfield] = ACTIONS(13),
    [anon_sym_newarray] = ACTIONS(13),
    [anon_sym_ldelem] = ACTIONS(13),
    [anon_sym_stelem] = ACTIONS(13),
    [anon_sym_i8] = ACTIONS(15),
    [anon_sym_i16] = ACTIONS(15),
    [anon_sym_i32] = ACTIONS(15),
    [anon_sym_i64] = ACTIONS(15),
    [anon_sym_u8] = ACTIONS(15),
    [anon_sym_u16] = ACTIONS(15),
    [anon_sym_u32] = ACTIONS(15),
    [anon_sym_u64] = ACTIONS(15),
    [anon_sym_f32] = ACTIONS(15),
    [anon_sym_f64] = ACTIONS(15),
    [anon_sym_str] = ACTIONS(15),
    [anon_sym_void] = ACTIONS(15),
  },
};

static uint16_t ts_small_parse_table[] = {
  [0] = 6,
    ACTIONS(17), 1,
      ts_builtin_sym_end,
    ACTIONS(19), 1,
      sym_identifier,
    STATE(2), 2,
      sym__nullary_instruction,
      sym__unary_instruction,
    ACTIONS(22), 3,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
    STATE(3), 3,
      sym_instruction,
      sym_label,
      aux_sym_statements_repeat1,
    ACTIONS(24), 27,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
  [50] = 6,
    ACTIONS(27), 1,
      ts_builtin_sym_end,
    ACTIONS(29), 1,
      sym_identifier,
    STATE(2), 2,
      sym__nullary_instruction,
      sym__unary_instruction,
    ACTIONS(31), 3,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
    STATE(3), 3,
      sym_instruction,
      sym_label,
      aux_sym_statements_repeat1,
    ACTIONS(33), 27,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
  [100] = 5,
    ACTIONS(29), 1,
      sym_identifier,
    STATE(25), 1,
      sym_statements,
    STATE(2), 2,
      sym__nullary_instruction,
      sym__unary_instruction,
    STATE(4), 3,
      sym_instruction,
      sym_label,
      aux_sym_statements_repeat1,
    ACTIONS(33), 27,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
  [145] = 2,
    ACTIONS(35), 1,
      ts_builtin_sym_end,
    ACTIONS(37), 31,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
      sym_identifier,
  [182] = 2,
    ACTIONS(39), 1,
      ts_builtin_sym_end,
    ACTIONS(41), 31,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
      sym_identifier,
  [219] = 2,
    ACTIONS(43), 1,
      ts_builtin_sym_end,
    ACTIONS(45), 31,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
      sym_identifier,
  [256] = 2,
    ACTIONS(47), 1,
      ts_builtin_sym_end,
    ACTIONS(49), 31,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
      anon_sym_halt,
      anon_sym_noop,
      anon_sym_add,
      anon_sym_sub,
      anon_sym_mul,
      anon_sym_div,
      anon_sym_mod,
      anon_sym_pop,
      anon_sym_testeq,
      anon_sym_testne,
      anon_sym_testlt,
      anon_sym_testgt,
      anon_sym_callvirt,
      anon_sym_ret,
      anon_sym_ldconst,
      anon_sym_ldlocal,
      anon_sym_stlocal,
      anon_sym_jmp,
      anon_sym_jmpt,
      anon_sym_jmpf,
      anon_sym_callfunc,
      anon_sym_newstruct,
      anon_sym_ldfield,
      anon_sym_stfield,
      anon_sym_newarray,
      anon_sym_ldelem,
      anon_sym_stelem,
      sym_identifier,
  [293] = 3,
    STATE(18), 1,
      sym_type,
    STATE(26), 1,
      sym__struct_types,
    ACTIONS(51), 12,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_str,
      anon_sym_void,
  [314] = 2,
    STATE(37), 1,
      sym_type,
    ACTIONS(51), 12,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_str,
      anon_sym_void,
  [332] = 2,
    STATE(22), 1,
      sym_type,
    ACTIONS(51), 12,
      anon_sym_i8,
      anon_sym_i16,
      anon_sym_i32,
      anon_sym_i64,
      anon_sym_u8,
      anon_sym_u16,
      anon_sym_u32,
      anon_sym_u64,
      anon_sym_f32,
      anon_sym_f64,
      anon_sym_str,
      anon_sym_void,
  [350] = 5,
    ACTIONS(55), 1,
      anon_sym_DASH,
    ACTIONS(57), 1,
      sym_dec_integer_literal,
    ACTIONS(59), 1,
      anon_sym_DQUOTE,
    ACTIONS(53), 4,
      sym_bin_integer_literal,
      sym_hex_integer_literal,
      sym_float_literal,
      sym_identifier,
    STATE(7), 4,
      sym__operand,
      sym__literal,
      sym__number_literal,
      sym_str_literal,
  [372] = 5,
    ACTIONS(55), 1,
      anon_sym_DASH,
    ACTIONS(59), 1,
      anon_sym_DQUOTE,
    ACTIONS(63), 1,
      sym_dec_integer_literal,
    ACTIONS(61), 4,
      sym_bin_integer_literal,
      sym_hex_integer_literal,
      sym_float_literal,
      sym_identifier,
    STATE(24), 4,
      sym__operand,
      sym__literal,
      sym__number_literal,
      sym_str_literal,
  [394] = 5,
    ACTIONS(65), 1,
      ts_builtin_sym_end,
    ACTIONS(67), 1,
      anon_sym_define,
    ACTIONS(70), 1,
      anon_sym_struct,
    ACTIONS(73), 1,
      anon_sym_func,
    STATE(15), 4,
      sym_definition,
      sym_struct,
      sym_function,
      aux_sym_start_repeat1,
  [413] = 5,
    ACTIONS(5), 1,
      anon_sym_define,
    ACTIONS(7), 1,
      anon_sym_struct,
    ACTIONS(9), 1,
      anon_sym_func,
    ACTIONS(76), 1,
      ts_builtin_sym_end,
    STATE(15), 4,
      sym_definition,
      sym_struct,
      sym_function,
      aux_sym_start_repeat1,
  [432] = 2,
    ACTIONS(80), 1,
      sym_dec_integer_literal,
    ACTIONS(78), 6,
      anon_sym_DASH,
      sym_bin_integer_literal,
      sym_hex_integer_literal,
      sym_float_literal,
      anon_sym_DQUOTE,
      sym_identifier,
  [444] = 3,
    ACTIONS(84), 1,
      anon_sym_COMMA,
    STATE(20), 1,
      aux_sym__struct_types_repeat1,
    ACTIONS(82), 4,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
  [457] = 1,
    ACTIONS(78), 6,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_EQ,
      anon_sym_struct,
      anon_sym_COMMA,
      anon_sym_func,
  [466] = 3,
    ACTIONS(84), 1,
      anon_sym_COMMA,
    STATE(21), 1,
      aux_sym__struct_types_repeat1,
    ACTIONS(86), 4,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
  [479] = 3,
    ACTIONS(90), 1,
      anon_sym_COMMA,
    STATE(21), 1,
      aux_sym__struct_types_repeat1,
    ACTIONS(88), 4,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
  [492] = 1,
    ACTIONS(88), 5,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_COMMA,
      anon_sym_func,
  [500] = 2,
    ACTIONS(95), 1,
      sym_dec_integer_literal,
    ACTIONS(93), 3,
      sym_bin_integer_literal,
      sym_hex_integer_literal,
      sym_float_literal,
  [509] = 1,
    ACTIONS(97), 4,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
  [516] = 1,
    ACTIONS(99), 4,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
  [523] = 1,
    ACTIONS(101), 4,
      ts_builtin_sym_end,
      anon_sym_define,
      anon_sym_struct,
      anon_sym_func,
  [530] = 1,
    ACTIONS(103), 1,
      anon_sym_COMMA,
  [534] = 1,
    ACTIONS(105), 1,
      sym_identifier,
  [538] = 1,
    ACTIONS(107), 1,
      anon_sym_DQUOTE,
  [542] = 1,
    ACTIONS(109), 1,
      anon_sym_args,
  [546] = 1,
    ACTIONS(111), 1,
      aux_sym_str_literal_token1,
  [550] = 1,
    ACTIONS(113), 1,
      anon_sym_EQ,
  [554] = 1,
    ACTIONS(115), 1,
      sym_dec_integer_literal,
  [558] = 1,
    ACTIONS(117), 1,
      sym_dec_integer_literal,
  [562] = 1,
    ACTIONS(119), 1,
      anon_sym_COLON,
  [566] = 1,
    ACTIONS(121), 1,
      anon_sym_EQ,
  [570] = 1,
    ACTIONS(123), 1,
      anon_sym_EQ,
  [574] = 1,
    ACTIONS(125), 1,
      anon_sym_locals,
  [578] = 1,
    ACTIONS(127), 1,
      ts_builtin_sym_end,
  [582] = 1,
    ACTIONS(129), 1,
      sym_identifier,
  [586] = 1,
    ACTIONS(131), 1,
      sym_identifier,
};

static uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(3)] = 0,
  [SMALL_STATE(4)] = 50,
  [SMALL_STATE(5)] = 100,
  [SMALL_STATE(6)] = 145,
  [SMALL_STATE(7)] = 182,
  [SMALL_STATE(8)] = 219,
  [SMALL_STATE(9)] = 256,
  [SMALL_STATE(10)] = 293,
  [SMALL_STATE(11)] = 314,
  [SMALL_STATE(12)] = 332,
  [SMALL_STATE(13)] = 350,
  [SMALL_STATE(14)] = 372,
  [SMALL_STATE(15)] = 394,
  [SMALL_STATE(16)] = 413,
  [SMALL_STATE(17)] = 432,
  [SMALL_STATE(18)] = 444,
  [SMALL_STATE(19)] = 457,
  [SMALL_STATE(20)] = 466,
  [SMALL_STATE(21)] = 479,
  [SMALL_STATE(22)] = 492,
  [SMALL_STATE(23)] = 500,
  [SMALL_STATE(24)] = 509,
  [SMALL_STATE(25)] = 516,
  [SMALL_STATE(26)] = 523,
  [SMALL_STATE(27)] = 530,
  [SMALL_STATE(28)] = 534,
  [SMALL_STATE(29)] = 538,
  [SMALL_STATE(30)] = 542,
  [SMALL_STATE(31)] = 546,
  [SMALL_STATE(32)] = 550,
  [SMALL_STATE(33)] = 554,
  [SMALL_STATE(34)] = 558,
  [SMALL_STATE(35)] = 562,
  [SMALL_STATE(36)] = 566,
  [SMALL_STATE(37)] = 570,
  [SMALL_STATE(38)] = 574,
  [SMALL_STATE(39)] = 578,
  [SMALL_STATE(40)] = 582,
  [SMALL_STATE(41)] = 586,
};

static TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_start, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [11] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_instruction, 1),
  [13] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_instruction, 1),
  [15] = {.entry = {.count = 1, .reusable = false}}, SHIFT(17),
  [17] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_statements_repeat1, 2),
  [19] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statements_repeat1, 2), SHIFT_REPEAT(35),
  [22] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_statements_repeat1, 2),
  [24] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statements_repeat1, 2), SHIFT_REPEAT(2),
  [27] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statements, 1),
  [29] = {.entry = {.count = 1, .reusable = false}}, SHIFT(35),
  [31] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_statements, 1),
  [33] = {.entry = {.count = 1, .reusable = false}}, SHIFT(2),
  [35] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__number_literal, 2),
  [37] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym__number_literal, 2),
  [39] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_instruction, 3),
  [41] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_instruction, 3),
  [43] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_str_literal, 3),
  [45] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_str_literal, 3),
  [47] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_label, 2),
  [49] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_label, 2),
  [51] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [53] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [55] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [57] = {.entry = {.count = 1, .reusable = false}}, SHIFT(7),
  [59] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [61] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [63] = {.entry = {.count = 1, .reusable = false}}, SHIFT(24),
  [65] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_start_repeat1, 2),
  [67] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_start_repeat1, 2), SHIFT_REPEAT(28),
  [70] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_start_repeat1, 2), SHIFT_REPEAT(41),
  [73] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_start_repeat1, 2), SHIFT_REPEAT(40),
  [76] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_start, 1),
  [78] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type, 1),
  [80] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_type, 1),
  [82] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__struct_types, 1),
  [84] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym__struct_types, 2),
  [88] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym__struct_types_repeat1, 2),
  [90] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym__struct_types_repeat1, 2), SHIFT_REPEAT(12),
  [93] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [95] = {.entry = {.count = 1, .reusable = false}}, SHIFT(6),
  [97] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_definition, 5),
  [99] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_function, 10, .production_id = 2),
  [101] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_struct, 3, .production_id = 1),
  [103] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [105] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [107] = {.entry = {.count = 1, .reusable = true}}, SHIFT(8),
  [109] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [111] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [113] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [115] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [117] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [119] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [121] = {.entry = {.count = 1, .reusable = true}}, SHIFT(34),
  [123] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [125] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [127] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [129] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [131] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef _WIN32
#define extern __declspec(dllexport)
#endif

extern const TSLanguage *tree_sitter_pylang2(void) {
  static TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .parse_table = (const uint16_t *)ts_parse_table,
    .parse_actions = ts_parse_actions,
    .lex_modes = ts_lex_modes,
    .alias_sequences = (const TSSymbol *)ts_alias_sequences,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .lex_fn = ts_lex,
    .keyword_lex_fn = ts_lex_keywords,
    .keyword_capture_token = sym_identifier,
    .field_count = FIELD_COUNT,
    .field_map_slices = (const TSFieldMapSlice *)ts_field_map_slices,
    .field_map_entries = (const TSFieldMapEntry *)ts_field_map_entries,
    .field_names = ts_field_names,
    .large_state_count = LARGE_STATE_COUNT,
    .small_parse_table = (const uint16_t *)ts_small_parse_table,
    .small_parse_table_map = (const uint32_t *)ts_small_parse_table_map,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .state_count = STATE_COUNT,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
