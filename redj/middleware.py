from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from threading import Lock
__obj_lock__= 1
__cache_handler__ = {}
__lock__ = Lock()
def detect_request(request_path):
    """
    Find app by request path
    :param path:
    :return:
    """


    from . import __apps_info__ as __apps__
    import os
    default_apps = [app for k,app in __apps__.items() if app.is_multi_tenancy==False and app.host == ""]
    default_app = None
    request_parts = [x for x in request_path.split('/') if x != ""]
    """
    check is existing app with host is empty (host at root)
    """
    if default_apps.__len__()>0:
        default_app = default_apps[0]
        if request_parts.__len__()==0: # request path is also root that means request match app
            file_path = os.path.join(default_app.dir,"index.html")
            return default_app ,"",file_path # return default app (app with host is emty),emptry tenancy and index.html path
    """
    Assume that request is call to app in the firts part of request
    Exmaple: '/app-admin/test.html' propally get content of test.html from app-admin app
    
    """
    if request_parts.__len__() ==0:
        return  None,None,None
    assume_app_name = request_parts[0]
    single_apps = [app for k, app in __apps__.items() if app.is_multi_tenancy == False and app.host.lower() == assume_app_name.lower()]
    if single_apps.__len__()>0:
        copy_request_parts = request_parts.copy()
        del copy_request_parts[0:1]
        file_path = os.path.join(single_apps[0].dir,os.path.sep.join(copy_request_parts))
        return  single_apps[0],None,file_path+".html"
    if request_parts.__len__()>1:
        assume_app_name = request_parts[1]
        multi_tenancy_apps = [app for k,app in __apps__.items() if app.is_multi_tenancy ==True and app.host.lower()==assume_app_name.lower()]
        if multi_tenancy_apps.__len__()>0:
            copy_request_parts = request_parts.copy()
            del copy_request_parts[0:2]
            file_path = os.path.join(multi_tenancy_apps[0].dir, os.path.sep.join(copy_request_parts))
            return multi_tenancy_apps[0],request_parts[0],file_path
    if default_app!=None:
        copy_request_parts = request_parts.copy()
        file_path = os.path.join(default_app.dir, os.path.sep.join(copy_request_parts))+".html"
        return default_app,None,file_path
    return None, None, None


class PreRequest:
    def __init__(self):
        self.rel_file_path = None
        self.app = None
        self.tenancy = None


class DynamicMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        global __obj_lock__
        global __cache_handler__
        if __cache_handler__.get(request.path) !=True:
            __lock__.acquire(__obj_lock__)
            try:
                app,tenancy,rel_file_path = detect_request(request.path)
                if app != None:
                    pre_request = PreRequest()
                    pre_request.tenancy= tenancy
                    pre_request.app =app
                    pre_request.rel_file_path=rel_file_path

                    __cache_handler__.update({request.path: pre_request})
                else:
                    __cache_handler__.update({request.path:True})
                __lock__.release()
            except Exception as ex:
                __lock__.release()
                raise  ex
        #resp = self.get_response(request)
        if __cache_handler__.get(request.path)==True:
            from django.http import Http404
            raise Http404
        pre_request = __cache_handler__.get(request.path)
        return  HttpResponse(
            "app_name="+pre_request.app.name +
            ",file_rel_path = "+ pre_request.rel_file_path+
            ", tenancy = "+ pre_request.tenancy
        )


    def process_request(self, request):

        return None