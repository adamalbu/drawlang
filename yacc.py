import ply.yacc as yacc
from lex import tokens
from colorama import Fore
import ast

py_ast = ast.Module(body=[], type_ignores=[])
fixed_setup = [
    ast.parse('import pygame').body[0],
    ast.parse('import pygame.gfxdraw').body[0],
    # pygame.init()
    ast.parse('pygame.init()').body[0],
    # __clock__ = pygame.time.Clock()
    ast.parse('__clock__ = pygame.time.Clock()').body[0],
    # __running__ = True
    ast.parse('__running__ = True').body[0],
]
user_setup = []

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_start(p):
    '''start : setup program
             | setup'''
    if len(p) == 3:
        # Wrap program commands inside a while loop
        loop_body = p[2]
    else:
        loop_body = p[1]

    # Create the while __running__ loop
    while_loop = ast.While(
        test=ast.Name(id='__running__', ctx=ast.Load()),
        body= [
            ast.parse('''for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                __running__ = False''').body[0],
        ] + loop_body + [
            ast.parse('pygame.display.flip()').body[0],
            ast.parse('__clock__.tick(60)').body[0]
        ],
        orelse=[]
    )

    # Combine fixed_setup, user_setup, and the while loop
    p[0] = fixed_setup + user_setup + [while_loop]

    global py_ast
    py_ast = ast.Module(
        body=p[0],
        type_ignores=[]
    )

def p_setup(p):
    '''setup : setup_cmd setup
             | setup_cmd'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Accumulate commands
    else:
        p[0] = [p[1]]  # Single command

    global user_setup
    user_setup = p[0]

def p_program(p):
    '''program : command program
               | command'''
    if len(p) == 3:
        p[0] = p[1] + p[2]  # Concatenate lists
    else:
        p[0] = p[1]  # p[1] is already a list

def p_canvas(p):
    '''setup_cmd : CANVAS STRING group2'''
    p[0] = ast.parse(f'__screen__ = pygame.display.set_mode(({p[3]}))').body[0]

def p_pos1(p):
    '''command : POS1 group2'''
    p[0] = ast.parse(f'__pos1__ = {p[2]}').body

def p_pos2(p):
    '''command : POS2 group2'''
    p[0] = ast.parse(f'__pos2__ = {p[2]}').body

def p_col(p):
    '''command : COL group3
               | COL STRING'''
    p[0] = ast.parse(f'__col__ = pygame.Color({p[2]})').body

def p_circle(p):
    '''command : CIRCLE NUM'''
    code = f'''pygame.gfxdraw.aacircle(__screen__, __pos1__[0], __pos1__[1], {p[2]}, __col__)
pygame.gfxdraw.filled_circle(__screen__, __pos1__[0], __pos1__[1], {p[2]}, __col__)'''
    p[0] = ast.parse(code).body  

def p_fill(p):
    '''command : FILL STRING
               | FILL group3'''
    p[0] = ast.parse(f'__screen__.fill({p[2]})').body

def p_sketch(p):
    'command : SKETCH expression'
    p[0] = ast.Expr(
        value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load()),
            args=[p[2]],
            keywords=[]
        )
    )

def p_assign(p):
    'command : ID EQUALS expression'
    p[0] = ast.Assign(
        targets=[ast.Name(id=p[1], ctx=ast.Store())],
        value=p[3]
    )

def p_load(p):
    'expression : ID'
    p[0] = ast.Name(id=p[1], ctx=ast.Load())

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | NUM'''
    if len(p) == 4:
        p[0] = ast.BinOp(
            left=p[1],
            op={
                '+': ast.Add(),
                '-': ast.Sub(),
                '*': ast.Mult(),
                '/': ast.Div(),
            }[p[2]],
            right=p[3]
        )
    else:
        p[0] = ast.Constant(value=p[1])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1][1:-1]  # Remove quotes

def p_group_tup3(p):
    '''group3 : LPAREN NUM NUM NUM RPAREN
              | NUM NUM NUM'''
    if len(p) == 6:
        p[0] = (p[2], p[3], p[4])
    else:
        p[0] = (p[1], p[2], p[3])

def p_group_tup2(p):
    '''group2 : LPAREN NUM NUM RPAREN
              | NUM NUM'''
    if len(p) == 5:
        p[0] = (p[2], p[3])
    else:
        p[0] = (p[1], p[2])

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

parser.parse(data, debug=1)

ast.fix_missing_locations(py_ast)
# print(ast.dump(py_ast, indent=4))

exec(compile(py_ast, filename='test', mode='exec'))
