from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from quikcy_controller import path_detector
from threading import Lock
from quikcy_controller.apps import on_apps_config_change
from quikcy_controller.template_render import render



class PreRequest:
    def __init__(self):
        self.rel_file_path = None
        self.app = None
        self.tenancy = None


class DynamicMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        template=path_detector.do_detect(request.path)
        if template!=None:
            html_content = render(template.rel_template_file_path)
            return HttpResponse(html_content)
        else:
            return self.get_response(request)

        # return  HttpResponse(
        #     "app_name="+pre_request.app.name +
        #     ",file_rel_path = "+ pre_request.rel_file_path+
        #     ",full_rel_path = " + full_file_path +
        #     ",has_extension="+str(has_extension)+
        #     ", tenancy = "+ str(pre_request.tenancy)
        # )


    def process_request(self, request):

        return None