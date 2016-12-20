from brb.utils import json_response
from rest_framework.authentication import SessionAuthentication


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return json_response({'detail': 'Unauthorised'}, status=401)
        return func(request, *args, **kwargs)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
