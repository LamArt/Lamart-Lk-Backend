from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from .models import ProviderToken

class TokenSerialiser(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token
    
class ProviderSerialiser(ModelSerializer):
    class Meta:
        model = ProviderToken
        fields = "__all__"