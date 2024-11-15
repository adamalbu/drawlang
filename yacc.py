import ply.yacc as yacc
from lex import tokens
from colorama import Fore
import ast

py_ast = ast.Module(body=[], type_ignores=[])

def p_program(p):
    'program : command'
    p[0] = ast.Module(
        body=[ast.Expr(value=p[1], lineno=1, col_offset=0)],
        type_ignores=[]
    )
    global py_ast
    py_ast = p[0]

def p_paint(p):
    'command : PAINT expression'
    p[0] = ast.Call(
        func=ast.Name(id='print', ctx=ast.Load(), lineno=1, col_offset=0),
        args=[p[2]],
        keywords=[],
        lineno=1,
        col_offset=0
    )

def p_string(p):
    'expression : STRING'
    p[0] = ast.Constant(value=p[1], lineno=1, col_offset=0)

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Example data
with open('main.fl', 'r') as file:
    data = file.read()

# Parse and generate the AST
parser.parse(data)

# Print the AST for debugging
print(ast.dump(py_ast, indent=4))

# Execute the AST
exec(compile(py_ast, filename='test', mode='exec'))
