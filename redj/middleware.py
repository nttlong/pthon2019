from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
class DynamicMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        return self.get_response(request)
    def process_request(self, request):
        print(request)
        print("OK")
        return None