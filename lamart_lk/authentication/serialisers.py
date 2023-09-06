from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from .models import ProviderToken
    
class ProviderSerialiser(ModelSerializer):
    class Meta:
        model = ProviderToken
        fields = ['access_token', 'organisation', 'provider']