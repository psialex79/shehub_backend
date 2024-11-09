from rest_framework import serializers
from .models import TelegramUser
from meetings.models import Meeting

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'time', 'place', 'invitee_name', 'description']

class TelegramUserSerializer(serializers.ModelSerializer):
    meetings = MeetingSerializer(many=True, read_only=True)

    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'first_name', 'last_name', 'username', 'registration_date', 'meetings']
