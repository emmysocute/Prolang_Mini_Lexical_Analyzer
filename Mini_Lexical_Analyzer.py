import sys
import os
import io
import argparse
from contextlib import redirect_stdout
from sly import Lexer

# Symbol Table
# datastructure section  ei ei
class MiniLexer(Lexer):

    # Token ที่เราต้องการ
    tokens = {INVALID_ID,IDENTIFIER,INTEGER, STRING, OPERATOR,LPAREN,RPAREN,SEMICOLON, KEYWORD}

    # ข้าม space และ tab
    ignore = ' \t'

    # Comment
    ignore_single_comment = r'//.*'

    @_(r'/\*[\s\S]*?\*/')
    def ignore_block_comment(self, t):
        self.lineno += t.value.count('\n')

    # newline
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # check identifier error
    @_(r'(_[a-zA-Z0-9]+|\d+[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z0-9_]*_[a-zA-Z0-9_]*)')
    def INVALID_ID(self, t):
        print(f'Lexical error: invalid identifier "{t.value}"')
        raise SystemExit
    
    def error(self, t):
        print(f'Lexical error: unexpected character "{t.value[0]}"')
        raise SystemExit


    # IDENTIFIER
    IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9]*'
    # Integer
    INTEGER = r'\d+'

    # String
    STRING = r'"[^"\n"]*"'

    # Operators (ordered longest-match first to avoid partial matches)
    # Arithmetic : +  -  *  / 
    # Comparison : ==   <  >  <=  >=
    
    @_(r'\+\+|--|==|<=|>=|[+\-*/=<>]')
    def OPERATOR(self, t):
        return t

    # Parentheses and Semicolon
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'


    # Keywords  
    IDENTIFIER['if']       = KEYWORD
    IDENTIFIER['then']     = KEYWORD
    IDENTIFIER['else']     = KEYWORD
    IDENTIFIER['endif']    = KEYWORD
    IDENTIFIER['while']    = KEYWORD
    IDENTIFIER['do']       = KEYWORD
    IDENTIFIER['endwhile'] = KEYWORD
    IDENTIFIER['print']    = KEYWORD
    IDENTIFIER['newline']  = KEYWORD
    IDENTIFIER['read']     = KEYWORD


def print_token(token, symbol_table):
    kind = token.type
    value = token.value

    if kind == "IDENTIFIER":
        if value in symbol_table:
            print(f'identifier "{value}" already in symbol table')
        else:
            symbol_table.add(value)
            print(f"new identifier: {value}")
    elif kind == "KEYWORD":
        print(f"keyword: {value}")
    elif kind == "INTEGER":
        print(f"integer: {value}")
    elif kind == "STRING":
        print(f"string: {value}")
    elif kind == "OPERATOR":
        print(f"operator: {value}")
    elif kind == "LPAREN":
        print("left parenthesis: (")
    elif kind == "RPAREN":
        print("right parenthesis: )")
    elif kind == "SEMICOLON":
        print("semicolon: ;")


    
# ส่วนตัดคำ 
parser = argparse.ArgumentParser(description="Mini Lexical Analyzer")
parser.add_argument("-i", required=True, help="Input source file")
parser.add_argument("-e", help="Expected output file (optional)")

args = parser.parse_args()

input_file = args.i
expect_file = args.e

# Check input file
if not os.path.isfile(input_file):
    print(f"File: {input_file} Not Found", file=sys.stderr)
    sys.exit(1)

# Read input source code
with open(input_file, "r", encoding="utf-8") as file:
    input_text = file.read()

# Read expected output only when -e is provided
expect_output = None

if expect_file is not None:
    if not os.path.isfile(expect_file):
        print(f"File: {expect_file} Not Found", file=sys.stderr)
        sys.exit(1)

    with open(expect_file, "r", encoding="utf-8") as file:
        expect_output = file.read()

lexer = MiniLexer()
symbol_table = set()

captured_output = io.StringIO()

try:
    with redirect_stdout(captured_output):
        for token in lexer.tokenize(input_text):
            print_token(token, symbol_table)
except SystemExit:
    print(captured_output.getvalue(), end="")
    sys.exit(1)


actual_output = captured_output.getvalue()
print("----------===== OUTPUT =====----------")
print(actual_output, end="")
print("----------==================----------")
print()
print()
print()
if expect_output is not None:
    actual = actual_output.replace("\r\n", "\n").rstrip("\n")
    expected = expect_output.replace("\r\n", "\n").rstrip("\n")

    if actual == expected:
        print("PASS: Output matches expected answer.")
    else:
        import difflib

        print("FAIL: Output does not match expected answer.",
              file=sys.stderr)

        diff = difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )

        for line in diff:
            print(line, file=sys.stderr)

        sys.exit(1)

