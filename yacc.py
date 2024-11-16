import ply.yacc as yacc
from lex import tokens
from colorama import Fore
import ast

py_ast = ast.Module(body=[], type_ignores=[])

fixed_setup = [
    ast.Import(names=[ast.alias(name='pygame')]),
    # pygame.init()
    ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='pygame', ctx=ast.Load()),
                attr='init',
                ctx=ast.Load()
            ),
            args=[],
            keywords=[]
        )
    ),
    # __clock__ = pygame.time.Clock()
    ast.Assign(
        targets=[ast.Name(id='__clock__', ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='pygame', ctx=ast.Load()),
                    attr='time',
                    ctx=ast.Load()
                ),
                attr='Clock',
                ctx=ast.Load()
            ),
            args=[],
            keywords=[]
        )
    ),
    # __running__ = True
    ast.Assign(
        targets=[ast.Name(id='__running__', ctx=ast.Store())],
        value=ast.Constant(value=True)
    ),
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
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         __running__ = False
            ast.For(
                target=ast.Name(id='event', ctx=ast.Store()),
                iter=ast.Call(
                    func=ast.Attribute(
                        value=ast.Attribute(
                            value=ast.Name(id='pygame', ctx=ast.Load()),
                            attr='event',
                            ctx=ast.Load()
                        ),
                        attr='get',
                        ctx=ast.Load()
                    ),
                    args=[],
                    keywords=[]
                ),
                body=[
                    ast.If(
                        test=ast.Compare(
                            left=ast.Attribute(
                                value=ast.Name(id='event', ctx=ast.Load()),
                                attr='type',
                                ctx=ast.Load()
                            ),
                            ops=[ast.Eq()],
                            comparators=[ast.Attribute(
                                value=ast.Name(id='pygame', ctx=ast.Load()),
                                attr='QUIT',
                                ctx=ast.Load()
                            )]
                        ),
                        body=[
                            ast.Assign(
                                targets=[ast.Name(id='__running__', ctx=ast.Store())],
                                value=ast.Constant(value=False)
                            )
                        ],
                        orelse=[]
                    )
                ],
                orelse=[]
            ),
        ] + loop_body + [
            # pygame.display.flip()
            ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Attribute(
                            value=ast.Name(id='pygame', ctx=ast.Load()),
                            attr='display',
                            ctx=ast.Load()
                        ),
                        attr='flip',
                        ctx=ast.Load()
                    ),
                    args=[],
                    keywords=[]
                )
            ),
            # __clock__.tick(60)
            ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id='__clock__', ctx=ast.Load()),
                        attr='tick',
                        ctx=ast.Load()
                    ),
                    args=[ast.Constant(value=60)],
                    keywords=[]
                )
            ),
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
    '''program : program command
               | command'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]  # Accumulate commands
    else:
        p[0] = [p[1]]  # Single command

def p_canvas(p):
    '''setup_cmd : CANVAS STRING TUP2'''
    p[0] = ast.parse(f'__screen__ = pygame.display.set_mode({p[3]})').body[0]

def p_fill(p):
    '''command : FILL STRING'''
    p[0] = ast.parse(f'__screen__.fill({p[2]})').body[0]

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
    p[0] = ast.Constant(value=p[1][1:-1])  # Remove quotes

def p_group_tup3(p):
    '''group3 : LPAREN NUM NUM NUM RPAREN
              | NUM NUM NUM'''
    if len(p) == 6:
        p[0] = ast.Constant(value=(p[2], p[3], p[4]))
    else:
        p[0] = ast.Constant(value=(p[1], p[2], p[3]))

# def p_group_tup2(p):
#     '''group2 : LPAREN NUM NUM RPAREN
#               | NUM NUM'''
#     if len(p) == 5:
#         p[0] = ast.Constant(value=(p[2], p[3]))
#     else:
#         p[0] = ast.Constant(value=(p[1], p[2]))

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

parser.parse(data)

ast.fix_missing_locations(py_ast)
print(ast.dump(py_ast, indent=4))

exec(compile(py_ast, filename='test', mode='exec'))
