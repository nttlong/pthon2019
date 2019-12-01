from enum import Enum
class DbTypes(Enum):
    POSTGRESQL="posgresl"
    MSSQL="mssql"
    MYSQL="mysql"

class DbContext:
    def __init__(self,
                 db_type=None,
                 connection_string=None,
                 db_name=None,
                 db_schema=None,
                 *args,**kwargs):
        assert isinstance(db_type,DbTypes)
        self.db_type=db_type
        self.connection_string= connection_string
        self.db_name=db_name
        self.db_schema=db_schema
        if isinstance(args,tuple) and len(args)>0:
            self.db_type=args[0]
            self.connection_string=args[1]

    def __enter__(self):
        from .query import Query
        return Query(self)
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

