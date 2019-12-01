from qsql.db_table import db_table
from qsql import query
@db_table("hr_employee")
class HR_Employee:
    Code=str,True,50
    Name=str,True,50


#print(HR_Employee.Code.name)
from qsql.db_context import DbContext
from qsql.db_context import DbTypes
from qsql.sql_compiler import compile_to_sql_string
with DbContext(db_type=DbTypes.POSTGRESQL,connection_string="") as qr:
    qr.select(HR_Employee).filter(HR_Employee.Name=="NV001")
    sql=compile_to_sql_string(qr)
    print(sql)