

class Query:
    def __init__(self,db_context):
        from .db_context import DbContext
        assert isinstance(db_context,DbContext)
        self.__selected_fields__=[]
        self.db_context= db_context
        self.db_schema= db_context.db_schema
        self.db_name= db_context.db_name
        self.alias_ticket=0
        self.source=None

    def get_selected_fiels(self):
        return self.__selected_fields__

    def set_db_schema(self,db_schema):
        assert isinstance(db_schema,str)
        self.db_schema=db_schema
        return self
    def get_source(self):
        from .sql_compiler import wrap_bracket_by_db_types as fn
        db_type=self.db_context.db_type
        if self.alias_ticket ==0:
            return fn(self.source, db_type)+" "+fn("T"+str(self.alias_ticket),db_type)



    def select(self,*args,**kwargs):
        """
        Select  fields
        :param args:
        :param kwargs:
        :return:
        """
        from .db_table import Field_Info,db_table
        fields=args
        if hasattr(args[0],"__is_table_info__"):
            fields=[]
            for f in args[0].__field_names__:
                fields.append(getattr(args[0],f).clone())


        for field in fields:
            assert isinstance(field,Field_Info)
            field.db_schema=self.db_schema
            field.db_type= self.db_context.db_type
            field.source="T"+str(self.alias_ticket)
            self.__selected_fields__.append(field)
        if self.alias_ticket==0:
            self.source = field.tabe_name
        return self

    def filter(self,*args,**kwargs):
        pass




