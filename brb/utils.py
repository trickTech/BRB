from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


def json_response(data, status=200, **kwargs):
    content = JSONRenderer().render(data)
    kwargs.pop('status', None)
    return HttpResponse(content, status=status, content_type="application/json", **kwargs)


def result_response(data, status=200, **kwargs):
    data = {'status': 'success', 'result': data}
    kwargs.pop('status', None)
    return json_response(data, **kwargs)


def error_response(error_info, status=500):
    error_body = {
        'status': 'fail',
        'result': error_info
    }

    return json_response(error_body, status=status)