from user.models import User
from rest_framework import serializers
from board.models import Event


class UserSerializer(serializers.ModelSerializer):
    # votes = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())

    class Meta:
        model = User
        fields = ('yiban_id', 'nickname', 'sex', 'events')
