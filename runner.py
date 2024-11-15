import ast

py_ast = ast.Module(
    body=[
        ast.Expr(
            value=ast.Call(
                func=ast.Name(id='print', ctx=ast.Load(), lineno=1, col_offset=0),
                args=[ast.Constant(value=6, lineno=1, col_offset=6)],
                keywords=[],
                lineno=1,
                col_offset=0
            ),
            lineno=1,
            col_offset=0
        )
    ],
    type_ignores=[]
)

exec(compile(py_ast, filename='test', mode='exec'))
