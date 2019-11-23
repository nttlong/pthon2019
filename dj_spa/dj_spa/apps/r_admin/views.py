"""
The declassification of views in app admin
    *index ->"index.html"
"""

from django.http import response, HttpResponse
def index(request):
    x=1
    print("OK")
    return  HttpResponse("OK sddfsafd")
