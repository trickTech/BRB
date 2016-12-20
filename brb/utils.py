from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import serializers


def json_response(data, status=200, **kwargs):
    content = JSONRenderer().render(data)
    kwargs.pop('status', None)
    return HttpResponse(content, status=status, content_type="application/json", **kwargs)


def result_response(data, status=200, **kwargs):
    return Response({'detail': data}, status=status, **kwargs)


def error_response(error_info, status=400):
    return result_response(error_info, status=status)


class CommonSerializer(serializers.Serializer):
    data = serializers.CharField(read_only=True)
