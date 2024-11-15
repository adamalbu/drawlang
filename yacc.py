import ply.yacc as yacc
from lex import tokens
from colorama import Fore
import ast

py_ast = ast.Module(body=[], type_ignores=[])

def p_program(p):
    '''program : program command
               | command'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]  # Accumulate commands
    else:
        p[0] = [p[1]]  # Single command

    global py_ast
    py_ast = ast.Module(
        body=p[0],
        type_ignores=[]
    )

def p_paint(p):
    'command : PAINT expression'
    p[0] = ast.Expr(
        value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load(), lineno=p.lineno(1), col_offset=p.lexpos(1)),
            args=[p[2]],
            keywords=[],
            lineno=p.lineno(1),
            col_offset=p.lexpos(1)
        ),
        lineno=p.lineno(1),
        col_offset=p.lexpos(1)
    )

def p_assign(p):
    'command : ID EQUALS expression'
    p[0] = ast.Assign(
        targets=[ast.Name(id=p[1], ctx=ast.Store(), lineno=p.lineno(1), col_offset=p.lexpos(1))],
        value=p[3],
        lineno=p.lineno(2),
        col_offset=p.lexpos(2)
    )

def p_load(p):
    'expression : ID'
    p[0] = ast.Name(id=p[1], ctx=ast.Load(), lineno=p.lineno(1), col_offset=p.lexpos(1))

def p_expression_string(p):
    'expression : STRING'
    p[0] = ast.Constant(value=p[1][1:-1], lineno=p.lineno(1), col_offset=p.lexpos(1))  # Remove quotes

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
compile(py_ast, filename='test', mode='exec')
# exec(compile(py_ast, filename='test', mode='exec'))
