from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .providers import YandexProvider, AtlassianProvider
from .serialisers import ProviderSerialiser, ExchangeCodeSerializer, RefreshAtlassianSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi

openapi_response_samples = {
    "201": openapi.Response(
        description="success",
        examples={
            "application/json": {
                "refresh": "string",
                "access": "string",
            }
        }
    )
}


class ExchangeProviderTokenView(APIView):
    @swagger_auto_schema(
        request_body=ProviderSerialiser,
        responses=openapi_response_samples,
        operation_id='Create JWT provider token',
        tags=['AUTH'],
        security=[None]
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
        print(user)
        print(provider.data)
        try:
            provider.save_provider_tokens(tokens, 5, user, request.data['provider'],
                                          request.data['organisation'])
        except KeyError:
            raise 'user tokens not be saved'

        return Response(tokens, status=status.HTTP_201_CREATED)


class ExchangeCodeToTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=ExchangeCodeSerializer,
        responses=openapi_response_samples,
        operation_id='Exchange authorization code to atlassian access and refresh token',
        tags=['AUTH'],
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

    @swagger_auto_schema(
        request_body=RefreshAtlassianSerializer,
        responses=openapi_response_samples,
        operation_id='Refresh to new refresh and access jira',
        tags=['AUTH'],
    )
    def post(self, request):
        try:
            provider = AtlassianProvider('atlassian')
        except KeyError:
            return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)
        print(request.user)
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
