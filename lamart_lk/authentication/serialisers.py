from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from .models import ProviderToken
from rest_framework import serializers


class ProviderInputSerializer(ModelSerializer):
    class Meta:
        model = ProviderToken
        exclude = ['user']


class ProviderSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, help_text="Refresh JWT token")
    access_token = serializers.CharField(required=True, help_text="Access JWT token")


class ExchangeCodeInputSerializer(serializers.Serializer):
    authorization_code = serializers.CharField(required=True, help_text="Atlassian authorization code")


class RefreshInputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, help_text="Atlassian refresh token")
