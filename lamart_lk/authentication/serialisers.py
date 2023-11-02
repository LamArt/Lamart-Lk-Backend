from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from .models import ProviderToken
from rest_framework import serializers


class ProviderSerialiser(ModelSerializer):
    class Meta:
        model = ProviderToken
        fields = ['access_token', 'organisation', 'provider']


class ExchangeCodeSerializer(serializers.Serializer):
    authorization_code = serializers.CharField(required=True, help_text="Jira authorization code")
