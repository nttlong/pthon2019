
def db_table(table_name,*args,**kwargs):
    class table_info:
        def __init__(self,data):
            self.__is_table_info__= True
            self.__field_names__=[]
            for k,v in data.items():
                self.__dict__.update({k:v})
                self.__field_names__.append(k)


    def wrapper(cls_object):
        from .sql_compiler import SqlMemberExpression,SqlExpression
        is_field=lambda x: x[0:2]!="__" and x[-2:]!="__"
        fields=[(k,*v) for (k,v) in cls_object.__dict__.items() if is_field(k)]
        init_dict={}
        for field in fields:

            field_info=Field_Info()
            field_info.name=field[0]
            field_info.type=field[1]
            field_info.is_require=field[2]
            field_info.max_len=field[3]
            field_info.tabe_name=table_name
            field_info.entity=cls_object

            init_dict.update({
                field[0]:field_info
            })

        return  table_info(init_dict)
    return wrapper

class Field_Info(object):
    def __init__(self):
        from .sql_compiler import SqlExpression,SqlMemberExpression
        self.name=""
        self.type=None
        self.is_require=False
        self.max_len=0
        self.tabe_name=""
        self.entity=None
        self.db_schema=None
        self.is_expression=False
        self.source=""
        self.owner=None
        self.db_type=None


    def clone(self):
        ret= Field_Info()
        for k,v in self.__dict__.items():
            if k[0:2]!="__" and k[-2]!="__":
                ret.__dict__.update({
                    k:v
                })
        return  ret
    def __repr__(self):
        from .sql_compiler import wrap_bracket_by_db_types as fn
        if self.expression!=None:
            return self.expression
        else:
            return fn(self.source,self.db_type)+"."+fn(self.name,self.db_type)

    def __eq__(self, other):
        from .sql_compiler import wrap_bracket_by_db_types as fn
        from .sql_compiler import SqlExpression,\
            SqlNullExpression,\
            SqlMemberExpression, \
            SqlValueExpression

        if other == None:
            expr= SqlExpression()
            expr.operator="IS"
            expr.right=SqlNullExpression()
            if self.expression!=None:
                expr.left=self.expression
            else:
                expr.left= SqlMemberExpression()
                expr.left.name=self.name
                expr.source=self.source
        else:
            expr = SqlExpression()
            expr.operator = "=="
            expr.right = SqlValueExpression()
            expr.right.value=other
            if self.expression != None:
                expr.left = self.expression
            else:
                expr.left = SqlMemberExpression()
                expr.left.name = self.name
                expr.source = self.source


        x=1