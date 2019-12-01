def __create_binary_expr__(operator,left,right):
    if isinstance(right, SqlExpr):
        return SqlBinaryExpr(operator, left, right)
    if not right and not isinstance(right,bool) :
        if operator!="=" and operator!="!=":
            raise Exception("Operator null is invalid. Pease, use == or !=")
        if operator=="=":
            return SqlBinaryExpr("is", left, SqlConstExpr(None))
        else:
            return SqlBinaryExpr("is not ", left, SqlConstExpr(None))
    else:
        return SqlBinaryExpr(operator, left, SqlConstExpr(right))
class SqlBaseExpr(object):
    def __getattr__(self, item):
        if item[0:2]!="__" and item[:-2]!="__":
            return SqlMemberExpr(item,self)
        else:
            return self.__dict__.get(item)
    def __str__(self):
        if isinstance(self,SqlNegativeExpr):
            return "(not "+self.expr.__str__()+")"
        if isinstance(self,SqlConstExpr):
            if self.value:
                if isinstance(self.__value__,str):
                    return "'"+self.__value__+"'"
                return str(self.__value__)
            else:
                return  "NULL"
        if isinstance(self,SqlMemberExpr):
            if not self.__expr__==None:
                return self.__name__
            return self.__expr__.__str__()+"."+self.__name__
        if isinstance(self,SqlBinaryExpr):
            if self.__left__.__str__()==None:
                return "(" + self.__left__.__str__() + " " + self.__operator__ + " " + self.__right__.__str__() + ")"
            return "("+ self.__left__.__str__()+" "+self.__operator__+" "+self.__right__.__str__()+")"
        if isinstance(self,SqlFuncExpr):
            return  self.__func_name__+"("+self.__expr__.__str__()+")"
        if isinstance(self,SqlArrayExpr):
            ret=""
            for x in self.__params__:
                ret+=x.__str__()+","
            return ret[:-1]
        else:

            return ""

    def __eq__(self, other):
        return __create_binary_expr__("=",self,other)
    def __ne__(self, other):
        return __create_binary_expr__("!=", self, other)

    def __and__(self, other):
        return __create_binary_expr__("and", self, other)
    def __or__(self, other):
        return __create_binary_expr__("or", self, other)
    def __add__(self, other):
        return __create_binary_expr__("+", self, other)
    def __sub__(self, other):
        return __create_binary_expr__("-", self, other)
    def __mul__(self, other):
        return __create_binary_expr__("*", self, other)
    def __divmod__(self, other):
        return __create_binary_expr__("%", self, other)

    def __le__(self, other):
        return __create_binary_expr__("<=", self, other)
    def __lt__(self, other):
        return __create_binary_expr__("<", self, other)
    def __ge__(self, other):
        return __create_binary_expr__(">=", self, other)
    def __gt__(self, other):
        return __create_binary_expr__(">=", self, other)
    def __floordiv__(self, other):
        return __create_binary_expr__("/", self, other)
    def __truediv__(self, other):
        return __create_binary_expr__("/", self, other)




class SqlExpr(SqlBaseExpr):
    def __init__(self):
        self.__type_name__= "SqlExpr"

class SqlConstExpr(SqlExpr):
    def __init__(self,value):
        super().__init__()
        self.__type_name__="SqlConstExpr"
        self.__value__=value
class SqlBinaryExpr(SqlExpr):
    def __init__(self,operator,left,right):
        super().__init__()
        self.__type_name__="SqlBinaryExpr"
        self.__left__=left
        self.__right__=right
        self.__operator__=operator


class SqlMemberExpr(SqlExpr):
    def __init__(self,name,expr):
        super().__init__()
        self.__type_name__= "SqlMemberExpr"
        self.__name__=name
        self.__expr__=expr

class SqlNegativeExpr(SqlExpr):
    def __init__(self,expr):
        super().__init__()
        self.__type_name__="SqlNegativeExpr"
        self.__expr__=expr

class SqlArrayExpr(SqlExpr):
    def __init__(self,lst,**kwargs):
        super().__init__()
        self.__type_name__="SqlArrayExpr"
        self.__params__=[]
        for x in lst:
            if isinstance(x,SqlExpr):
                self.__params__.append(x)
            else:
                self.__params__.append(SqlConstExpr(x))


class SqlFuncExpr(SqlExpr):
    def __init__(self,func_name,*args,**kwargs):
        super().__init__()
        self.__type_name__="SqlFuncExpr"
        self.__func_name__=func_name
        if args.__len__()==1:
            expr=args[0]
            if isinstance(expr,tuple):
                self.expr=SqlArrayExpr(expr)
            elif isinstance(expr,SqlExpr):
                self.__expr__=expr
            else:
                self.__expr__=SqlConstExpr(expr)
        else:
            self.__expr__=SqlArrayExpr(list(args))