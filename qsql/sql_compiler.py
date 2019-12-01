


def get_default_schema(db_type):
    from .db_context import DbTypes
    assert isinstance(db_type,DbTypes)
    if db_type== DbTypes.POSTGRESQL:
        return "public"
    if db_type== DbTypes.MSSQL:
        return "dbo"
    else:
        raise  NotImplemented()
def get_sql_db_type_bracket(db_type):
    from .db_context import DbTypes
    assert isinstance(db_type, DbTypes)
    if db_type==DbTypes.MSSQL:
        return "[]"
    if db_type == DbTypes.POSTGRESQL:
        return "\"\""
    if db_type == db_type.MYSQL:
        return "``"
def get_full_field_name(field,bracket="\"\""):
    from .db_table import  Field_Info
    assert isinstance(field,Field_Info)
    if not field.is_expression:
        return bracket[0]+field.source+bracket[1]+"."+bracket[0]+field.name+bracket[1]
    return field.field
def wrap_bracket_by_db_types(str_name,db_type):
    from .db_context import DbTypes
    assert isinstance(db_type, DbTypes)
    brackets= get_sql_db_type_bracket(db_type)
    return brackets[0]+str_name+brackets[1]

def compile_to_sql_string(qr):
    from .query import Query
    assert isinstance(qr,Query)
    ret_sql="select "
    for f in qr.__selected_fields__:
        ret_sql+=get_full_field_name(f)+","
    ret_sql = ret_sql[:-1]
    ret_sql += " from "+qr.get_source()
    return ret_sql



