from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from quikcy_controller import path_detector
from threading import Lock
from quikcy_controller.apps import on_apps_config_change
from quikcy_controller.template_render import render
__lock__ = Lock()
__cache_handler__ = {}
__obj_lock__ =1
def __clear_cache_when_app_config_file_change__():
    global __cache_handler__
    __cache_handler__ = {}
on_apps_config_change(__clear_cache_when_app_config_file_change__)
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
                app,tenancy,rel_file_path,full_file_path,has_extension = path_detector.do_detect(request.path)
                if app != None:
                    pre_request = PreRequest()
                    pre_request.tenancy= tenancy
                    pre_request.app =app
                    pre_request.rel_file_path= rel_file_path


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
        #html_content = render(pre_request.rel_file_path)
        return  HttpResponse(
            "app_name="+pre_request.app.name +
            ",file_rel_path = "+ pre_request.rel_file_path+
            ",full_rel_path = " + full_file_path +
            ",has_extension="+str(has_extension)+
            ", tenancy = "+ str(pre_request.tenancy)
        )


    def process_request(self, request):

        return None