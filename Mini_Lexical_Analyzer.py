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
    # Arithmetic : +  -  *  /  %  **
    # Comparison : ==  !=  <  >  <=  >=
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




    
# ส่วนตัดคำ 
lexer = MiniLexer()

with open("input.txt", "r", encoding="utf-8") as file:
    text = file.read()
# text = '123'

for token in lexer.tokenize(text):
    print(token.type.lower(),":", token.value)