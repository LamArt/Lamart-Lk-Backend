from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .providers import YandexProvider, AtlassianProvider
from .serialisers import ProviderSerialiser, ExchangeCodeSerializer, RefreshAtlassianSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


class ExchangeProviderTokenView(APIView):
    @extend_schema(
        request=ProviderSerialiser,
        responses={201: OpenApiTypes.OBJECT},
        summary='Create JWT provider token',
        description='Takes provider JWT token, organisation returns access and refresh JWT tokens',
        tags=['auth'],
    )
    def post(self, request):
        try:
            provider = YandexProvider(request.data['provider'])
        except KeyError:
            return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)

        try:
            provider_token = request.data['access_token']
            provider.get_data(provider_token)
        except KeyError:
            return Response('token is not valid', status=status.HTTP_400_BAD_REQUEST)

        try:
            provider.check_organisation(request.data['organisation'])
        except KeyError:
            return Response(f"organisation {request.data['organisation']} is not supported")
        except ValueError:
            return Response(
                f"organisation {request.data['organisation']} don't have @{provider.data['default_email'].split('@')[1]} domain")

        refresh = RefreshToken.for_user(provider.get_user())
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        user = provider.get_user()
        try:
            provider.save_provider_tokens(tokens, 5, user, request.data['provider'],
                                          request.data['organisation'])
        except KeyError:
            raise 'user tokens not be saved'

        return Response(tokens, status=status.HTTP_201_CREATED)


class ExchangeCodeToTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ExchangeCodeSerializer,
        responses={201: OpenApiTypes.OBJECT},
        summary='Exchange code to atlassian JWT token',
        description='Takes authorization code, returns atlassian access and refresh JWT tokens',
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
            'access': access_token,
            'refresh': refresh_token,
        }
        try:
            provider.save_provider_tokens(tokens, provider.data['expires_in'],
                                          request.user, 'atlassian', 'lamart')
        except KeyError:
            raise 'user tokens not be saved'

        return Response(tokens, status=status.HTTP_201_CREATED)


class RefreshAtlassianView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=RefreshAtlassianSerializer,
        responses={201: OpenApiTypes.OBJECT},
        summary='Refresh atlassian JWT token',
        description='Takes refresh JWT token, returns new access and refresh JWT tokens',
        tags=['auth'],
    )
    def post(self, request):
        try:
            provider = AtlassianProvider('atlassian')
        except KeyError:
            return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh_token = request.data['refresh_token']
            provider.refresh(refresh_token)
            access_token = provider.data['access_token']
            refresh_token = provider.data['refresh_token']
        except KeyError:
            return Response('not valid authorization code', status=status.HTTP_400_BAD_REQUEST)

        tokens = {
            'access': access_token,
            'refresh': refresh_token,
        }
        try:
            provider.save_provider_tokens(tokens, provider.data['expires_in'],
                                          request.user, 'atlassian', 'lamart')
        except KeyError:
            raise 'user tokens not be saved'
        return Response(tokens, status=status.HTTP_201_CREATED)
