__result_cahce__ = {}

def fn_cacher(*args,**kwargs):
    fn = args[0]
    def wrapper(*args,**kwargs):
        global __result_cahce__
        import json
        key = json.dumps(args)+"@"+json.dumps(kwargs)
        try:
            return __result_cahce__[key]
        except KeyError:
            __result_cahce__[key] = fn(*args,**kwargs)
        except Exception as ex:
            raise ex
        return __result_cahce__[key]
    return wrapper
