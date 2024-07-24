# myapp/serializers.py
from rest_framework import serializers

class SMSSerializer(serializers.Serializer):
    text = serializers.CharField()
