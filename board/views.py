from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from board.serializers import EventSerializer, VoteSerializer
import functools
from .models import Event


# Create your views here.


def json_response(data, **kwargs):
    content = JSONRenderer().render(data)
    response = HttpResponse(content, content_type="application/json", **kwargs)
    return response


def cross_site(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Credentials"] = True
        response["Access-Control-Max-Age"] = '86400'
        response["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
        return response

    return _wrapper


@cross_site
def event_list(request):
    if request.method == 'OPTIONS':
        return HttpResponse('', status=200)
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return json_response(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return json_response(serializer.data, status=201)
        return json_response(serializer.errors, status=400)


@cross_site
def event_detail(request, pk):
    if request.method == 'OPTIONS':
        return HttpResponse('', status=200)
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return json_response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return json_response(serializer.data)
        return json_response(serializer.errors, status=400)


@cross_site
def vote(request, pk):
    if request.method == 'OPTIONS':
        return HttpResponse('', status=200)
    if request.method == 'POST':
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return HttpResponse(status=404)

        data = JSONParser().parse(request)
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            event.vote += serializer.data.get('vote')
            event.save()
            return json_response(serializer.data)
        return json_response(serializer.errors, status=400)

    return HttpResponse(status=404)
