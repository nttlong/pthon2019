from qsql.db_table import db_table
@db_table("hr_employee")
class HR_Employee:
    Code=str,True,50
    Name=str,True,50


print(HR_Employee.Code.name)