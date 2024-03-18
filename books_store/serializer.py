from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
