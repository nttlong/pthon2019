
def db_table(table_name,*args,**kwargs):
    class table_info:
        def __init__(self,data):
            for k,v in data.items():
                self.__dict__.update({k:v})


    def wrapper(cls_object):
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
            init_dict.update({
                field[0]:field_info
            })

        return  table_info(init_dict)
    return wrapper

class Field_Info:
    def __init__(self):
        self.name=""
        self.type=None
        self.is_require=False
        self.max_len=0
        self.tabe_name=""