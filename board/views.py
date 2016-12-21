import json

from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView

import django_filters.rest_framework

from brb.utils import error_response, json_response
from brb.auth import CsrfExemptSessionAuthentication
from brb.mixins import ViewSearchMixin

from board.serializers import EventSerializer
from board.models import Event, Vote
from board.permissions import IsOwnerOrReadOnly


class EventList(ViewSearchMixin, generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    object_model = Event

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            event_list = serializer.data
            for event in event_list:
                event['vote_status'] = 0
            event_map = {event['id']: index for index, event in enumerate(event_list)}

            if request.user.is_authenticated():
                vote_records = Vote.objects.values_list('event_id', 'vote').filter(
                    event_id__in=event_map.keys(), author=request.user).all()
                for vote in vote_records:
                    index = event_map[vote[0]]
                    event_list[index]['vote_status'] = vote[1]

            return self.get_paginated_response(event_list)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_delete:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if self.request.user.is_admin:
            instance.is_delete = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class VoteView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None, pk=None):
        pk = self.kwargs['pk']
        try:
            info = json.loads(request.body.decode())
            vote_value = int(info['vote_value'])
        except Exception as exc:
            return error_response('bad request (bad json)', status=status.HTTP_400_BAD_REQUEST)

        if vote_value not in [1, -1]:
            return error_response('bad request (bad vote value)', status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.filter(pk=pk).first()

        if not event:
            return error_response('not found', status=status.HTTP_404_NOT_FOUND)

        vote = Vote.objects.filter(author=request.user, event=pk).first()

        if vote:
            event.vote_count -= vote.vote
            event.vote_count += vote_value

            vote.vote = vote_value
            event.save()
            vote.save()
        else:
            event.vote_count += vote_value
            vote = Vote.objects.create(author=request.user, event=event)
            event.save()

        return json_response(
            {'event': pk,
             'user': request.user.id,
             'vote_value': vote_value,
             'vote_count': event.vote_count})
