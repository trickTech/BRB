from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=20)
    content = serializers.CharField(required=True, allow_blank=True, max_length=65535)
    event_type = serializers.ChoiceField(choices=[0, 1], required=True, allow_blank=False)

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)

        instance.save()
        return instance
