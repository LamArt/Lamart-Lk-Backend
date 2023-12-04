from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from .models import ProviderToken
from rest_framework import serializers


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = ProviderToken
        exclude = ['user']


class TokensSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
