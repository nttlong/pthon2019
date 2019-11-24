from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from threading import Lock
from .apps import on_apps_config_change
from .apps import get_root_dir
import os

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
    extension_of_path = request_path.split(".")[-1]
    has_extesion = False
    if extension_of_path != request_path:
        has_extesion = True
        request_path = request_path[0:len(request_path) - len(extension_of_path)-1]

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
            full_file_path = os.path.join(get_root_dir(),file_path)
            if not os.path.exists(full_file_path):
                return None,None,None,None,None
            return default_app, "", file_path,full_file_path, False  # return default app (app with host is emty),emptry tenancy and index.html path

    """
    Assume that request is call to app in the firts part of request
    Exmaple: '/app-admin/test.html' propally get content of test.html from app-admin app

    """
    not_check_file_path =False
    if request_parts.__len__() == 0:
        return None, None, None, None
    assume_app_name = request_parts[0]
    single_apps = [app for k, app in __apps__.items() if
                   app.is_multi_tenancy == False and app.host.lower() == assume_app_name.lower()]
    if single_apps.__len__() > 0:
        copy_request_parts = request_parts.copy()
        del copy_request_parts[0:1]
        file_path = os.path.join(single_apps[0].dir, os.path.sep.join(copy_request_parts))
        if has_extesion:
            file_path += "."+extension_of_path
        full_file_path = os.path.join(get_root_dir(), file_path)
        if os.path.exists(full_file_path) or not_check_file_path:
            return single_apps[0], None, file_path ,full_file_path,has_extesion
        else:
            return None,None,None,None,None

    if request_parts.__len__() > 1:
        assume_app_name = request_parts[1]
        multi_tenancy_apps = [app for k, app in __apps__.items() if
                              app.is_multi_tenancy == True and app.host.lower() == assume_app_name.lower()]
        if multi_tenancy_apps.__len__() > 0:
            copy_request_parts = request_parts.copy()
            if not has_extesion:
                del copy_request_parts[0:2]
                if copy_request_parts.__len__()==0:
                    copy_request_parts=["index"]
                file_path = os.path.join(multi_tenancy_apps[0].dir.replace('/',os.path.sep), os.path.sep.join(copy_request_parts))+".html"
            else:
                file_path = os.path.join(multi_tenancy_apps[0].dir.replace('/',os.path.sep), os.path.sep.join(copy_request_parts)) + "."+extension_of_path
            full_file_path = os.path.join(get_root_dir(), file_path)
            if os.path.exists(full_file_path) :
                return multi_tenancy_apps[0], request_parts[0], file_path,full_file_path,False



    if default_app != None:
        copy_request_parts = request_parts.copy()
        file_path = os.path.join(default_app.dir.replace('/',os.path.sep), os.path.sep.join(copy_request_parts))
        if has_extesion:
            file_path+= "."+extension_of_path
        full_file_path = os.path.join(get_root_dir(), file_path)
        if os.path.exists(full_file_path)  or not_check_file_path:
            return default_app, None, file_path,full_file_path,has_extesion
        else:
            return None,None,None,None, None
    return None, None, None

"""
        file_path= os.path.sep.join(request_parts)
        file_path_full =os.sep.join([get_root_dir(),default_app.dir.replace('/',os.path.sep),file_path])
        if has_extesion:
            file_path_full+="."+extension_of_path;
        else:
            file_path_full+=".html"
        if os.path.exists(file_path_full):
            return default_app,"",file_path,file_path_full,has_extesion
"""