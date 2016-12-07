import json

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from rest_framework.authentication import BasicAuthentication
from brb.utils import error_response
from board.serializers import EventSerializer, VoteSerializer

from .models import Event, Vote
from .permissions import IsOwnerOrReadOnly, login_required
from brb.auth import CsrfExemptSessionAuthentication


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@login_required
def vote(request, pk):
    if request.method == 'POST':
        try:
            info = json.loads(request.body)
            vote_value = info['vote_value']
        except Exception as exc:
            return error_response({'bad request'}, status=400)

        event = Event.objects.filter(pk=pk).first()

        if not event:
            return error_response('not found', status=404)

        vote = Vote.objects.filter(author=request.user, event=pk).first()

        if vote:
            event -= vote.vote
            event += vote_value

            vote.vote = vote_value
            event.save()
            vote.save()
        else:
            event += vote_value
            vote = Vote.objects.create(author=request.user, event=event)

        return

    return error_response({'detail': 'Method not allowed.'}, status=405)
