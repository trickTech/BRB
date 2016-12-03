import json
import urllib.request
from django.http import HttpResponse
import binascii
from .user_const import (
    USER_ACCESS_URL,
    APPID,
    APPSECRET
)
from Crypto.Cipher import AES
from brb.utils import (
    json_response,
    error_response,
)


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


def auth(request):
    if request.method == 'POST':
        token = request.FORM.get('access_token')
        if token is None:
            return error_response('token not valid')
        return json_response({'result': token})


def is_login(request):
    result = request.user.is_authenticated()
    return json_response({'is_login': result})


def _decode_access_token(token):
    content = binascii.hexlify(token)

    key = binascii.unhexlify(APPSECRET)
    IV = APPID
    mode = AES.MODE_CBC

    encryptor = AES.new(key, mode, IV=IV)
    real_content = binascii.hexlify(encryptor.encrypt(content))

    return real_content
