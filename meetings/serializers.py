from rest_framework import serializers
from .models import Meeting

class MeetingSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Meeting
        fields = ['id', 'invitee_name', 'place', 'date', 'time', 'isNew', 'author']
        read_only_fields = ['id', 'isNew', 'author']
