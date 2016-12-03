from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


def json_response(data, status=200, **kwargs):
    content = JSONRenderer().render(data)
    kwargs.pop('status', None)
    response = HttpResponse(content, status=status, content_type="application/json", **kwargs)
    return response


def error_response(error_info, status=500):
    error_body = {
        'status': 'fail',
        'msg': error_info
    }

    return json_response(error_body, status=status)
