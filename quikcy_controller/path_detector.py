from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from threading import Lock
from .apps import on_apps_config_change



 #install clear cache watcher
__obj_lock__ = 1 #lock muti theads access floag
__cache_handler__ = {} #cache handler path
__lock__ = Lock()

def __clear_cache_when_apps_config_change__():
    """
    Clear cache whenever json file of apps has been change
    :return:
    """
    global __cache_handler__
    __cache_handler__ = {}
on_apps_config_change(__clear_cache_when_apps_config_change__)

def cache_func(*args,**kwargs):
    fn_call=args[0]
    def wrapper(request_path):
        global __cache_handler__
        global __obj_lock__
        if __cache_handler__.get(request_path.lower()) == None:
            __lock__.acquire(__obj_lock__)
            try:
                __cache_handler__.update(
                    {
                        request_path.lower(): fn_call(request_path)
                    }
                )
                __lock__.release()
            except Exception as ex:
                __lock__.release()
                raise ex
        return __cache_handler__[request_path]
    return wrapper
@cache_func
def do_detect(request_path):
    """
    Detect a request path if it is in app and has a resource content file
    :param path:
    :return:
    """

    from . apps import get_all_apps
    import os
    __apps__ = get_all_apps()
    default_apps = [app for k, app in __apps__.items() if app.is_multi_tenancy == False and app.host == ""]
    default_app = None
    request_parts = [x for x in request_path.split('/') if x != ""]
    """
    check is existing app with host is empty (host at root)
    """
    if default_apps.__len__() > 0:
        default_app = default_apps[0]
        if request_parts.__len__() == 0:  # request path is also root that means request match app
            file_path = os.path.join(default_app.dir, "index.html")
            return default_app, "", file_path  # return default app (app with host is emty),emptry tenancy and index.html path
    """
    Assume that request is call to app in the firts part of request
    Exmaple: '/app-admin/test.html' propally get content of test.html from app-admin app

    """
    if request_parts.__len__() == 0:
        return None, None, None
    assume_app_name = request_parts[0]
    single_apps = [app for k, app in __apps__.items() if
                   app.is_multi_tenancy == False and app.host.lower() == assume_app_name.lower()]
    if single_apps.__len__() > 0:
        copy_request_parts = request_parts.copy()
        del copy_request_parts[0:1]
        file_path = os.path.join(single_apps[0].dir, os.path.sep.join(copy_request_parts))
        return single_apps[0], None, file_path + ".html"
    if request_parts.__len__() > 1:
        assume_app_name = request_parts[1]
        multi_tenancy_apps = [app for k, app in __apps__.items() if
                              app.is_multi_tenancy == True and app.host.lower() == assume_app_name.lower()]
        if multi_tenancy_apps.__len__() > 0:
            copy_request_parts = request_parts.copy()
            del copy_request_parts[0:2]
            if copy_request_parts.__len__()==0:
                copy_request_parts=["index.html"]
            file_path = os.path.join(multi_tenancy_apps[0].dir, os.path.sep.join(copy_request_parts))
            return multi_tenancy_apps[0], request_parts[0], file_path
    if default_app != None:
        copy_request_parts = request_parts.copy()
        file_path = os.path.join(default_app.dir, os.path.sep.join(copy_request_parts)) + ".html"
        return default_app, None, file_path
    return None, None, None