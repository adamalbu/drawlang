import ply.lex as lex

reserved = {
    'sketch' : 'SKETCH',
    'canvas' : 'CANVAS',
    'pos1' : 'POS1',
    'pos2' : 'POS2',
    'col' : 'COL',

    'fill': 'FILL',
    'circle': 'CIRCLE',
}

# List of token names.   This is always required
tokens = (
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'NUM',
    'STRING',
    'ID',
    # 'TUP2',
    # 'TUP3',
    'NEWLINE',
) + tuple(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='

# Regular expression rules for simple tokens

# def t_TUP2(t):
#     r'\(\d+\s\d+\)'
#     t.value = tuple(map(int, t.value[1:-1].split()))
#     return t  

# def t_TUP3(t):
#     r'\(\d+\s\d+\s\d+\)'
#     t.value = tuple(map(int, t.value[1:-1].split()))
#     return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
with open('main.fl', 'r') as file:
    data = file.read()
lexer.input(data)

if __name__ == '__main__':
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
else:
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input