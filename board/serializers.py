from .models import Event, Vote
from user.models import User
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'content', 'author', 'event_type', 'vote_count', 'created_at', 'updated_at')

    event_type = serializers.ChoiceField(choices=[0, 1], required=True)
    author = serializers.ReadOnlyField(source='author.nickname')
    vote_count = serializers.ReadOnlyField()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'event', 'vote', 'author', 'created_at')

    event = serializers.PrimaryKeyRelatedField(many=False, queryset=Event.objects.all())
    vote = serializers.ChoiceField(choices=[0, 1, -1], required=True)
