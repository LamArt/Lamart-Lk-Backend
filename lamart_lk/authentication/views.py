from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status, permissions
from authentication.providers.base import YandexProvider, AtlassianProvider
from .serialisers import TokensSerializer, ProviderSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, inline_serializer


class ExchangeProviderTokenView(APIView):
    serializer_class = ProviderSerializer

    @extend_schema(
        responses=TokensSerializer,
        summary='Create JWT provider',
        description='Takes provider JWT, organisation returns access and refresh JWT',
        tags=['auth'],
    )
    def post(self, request):
        try:
            provider = YandexProvider(request.data['provider'])
        except KeyError:
            return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)

        try:
            provider.get_data(request.data['access_token'])
        except KeyError:
            return Response('token is not valid', status=status.HTTP_400_BAD_REQUEST)

        try:
            provider.check_organisation(request.data['organisation'])
        except KeyError:
            return Response(f"organisation {request.data['organisation']} is not supported")
        except ValueError:
            # organisation checking is disabled during DEBUG
            return Response(
                f"organisation {request.data['organisation']} don't have @{provider.data['default_email'].split('@')[1]} domain",
                status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(provider.get_user())
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        try:
            refresh_token = tokens['refresh_token']
        except KeyError:
            refresh_token = None

        try:
            provider.save_provider_tokens({'access': request.data['access_token'], 'refresh': refresh_token},
                                          request.data['expires_in'], provider.get_user(), request.data['provider'],
                                          request.data['organisation'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(tokens, status=status.HTTP_201_CREATED)


class ExchangeCodeToTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = inline_serializer(name='CodeExchangeSerializer',
                                         fields={'authorization_code': serializers.CharField()})

    @extend_schema(
        responses=TokensSerializer,
        summary='Exchange code to atlassian JWT',
        description='Takes authorization code, returns atlassian access and refresh JWT',
        tags=['auth'],
    )
    def post(self, request):
        try:
            provider = AtlassianProvider('atlassian')
        except KeyError:
            return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)
        try:
            authorization_code = request.data['authorization_code']
            provider.get_data(authorization_code)
            access_token = provider.data['access_token']
            refresh_token = provider.data['refresh_token']
        except KeyError:
            return Response('not valid authorization code', status=status.HTTP_400_BAD_REQUEST)

        tokens = {
            'refresh': refresh_token,
            'access': access_token,
        }
        try:
            provider.save_provider_tokens(tokens, provider.data['expires_in'],
                                          request.user, 'atlassian', 'lamart')
        except KeyError:
            return Response('user tokens not be saved', status=status.HTTP_400_BAD_REQUEST)

        return Response(tokens, status=status.HTTP_201_CREATED)
