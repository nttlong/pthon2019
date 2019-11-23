"""
The declassification of views in app admin
    *index ->"index.html"
"""

from django.http import response, HttpResponse
def index(request):
    return  HttpResponse("OK")
