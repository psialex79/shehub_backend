from rest_framework import serializers

class GreetingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    message = serializers.CharField(max_length=200)
