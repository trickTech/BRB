import json
import urllib.request
from django.http import HttpResponse
from django.shortcuts import render

from .const import USER_ACCESS_URL


# Create your views here.

def callback_handler(request):
    if request.method == "GET":
        code = request.GET.get('code')
        if not code:
            return HttpResponse(status=404)
        else:
            try:
                http_response = urllib.request.urlopen(USER_ACCESS_URL % code).read().decode('utf8')
                data = json.loads(http_response)
                return HttpResponse(str(data))
            except Exception:
                return HttpResponse("Net Error")
    return HttpResponse(status=404)
