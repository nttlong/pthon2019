def Not(expr):

    from .expressions import SqlNegativeExpr
    return SqlNegativeExpr(expr)

def And(*args,**kwargs):
    pass
def Concat(*args,**kwargs):
    from .expressions import SqlFuncExpr
    x=str(args[0])
    return SqlFuncExpr("concat",*args,**kwargs)