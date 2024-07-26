from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email"]

    username = serializers.CharField()
