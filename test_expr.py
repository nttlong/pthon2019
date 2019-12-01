from qsql.expressions import *
from qsql.sql_funcs import *
x=SqlExpr()

y=Concat(x.emps.code," ",x.emps.name)

print(y)