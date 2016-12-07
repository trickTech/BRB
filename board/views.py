from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from board.serializers import EventSerializer, VoteSerializer

from .models import Event, Vote
from .permissions import IsOwnerOrReadOnly


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class VoteList(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        pass
