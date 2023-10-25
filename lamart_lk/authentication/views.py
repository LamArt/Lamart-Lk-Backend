from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, api_view
from .providers import Provider
from .serialisers import *
from rest_framework import status
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken

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


@authentication_classes([])
@swagger_auto_schema(
    method='post',
    request_body=ProviderSerialiser,  # query_serializer
    responses=openapi_response_samples,
    __name__='exchange_token',
    operation_id='Create JWT token',
    tags=['AUTH'],
    security=[None]
)
@api_view(['POST'])
def exchange_token(request, *args, **kwargs):
    """Takes provider JWT, organisation returns access and refresh JWT"""

    # validating provider
    try:
        provider = Provider(request.data['provider'])
    except KeyError:
        return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)

    # validating token
    try:
        provider_token = request.data['access_token']
        provider.get_data(provider_token)
    except KeyError:
        return Response('token is not valid', status=status.HTTP_400_BAD_REQUEST)

    # validating organisation and email domain
    try:
        provider.check_organisation(request.data['organisation'])
    except KeyError:
        return Response(f"organisation {request.data['organisation']} is not supperted")
    except ValueError:
        return Response(
            f"organisation {request.data['organisation']} don't have @{provider.data['default_email'].split('@')[1]} domain")

    # generate tokens
    refresh = RefreshToken.for_user(provider.get_user())
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return Response(tokens, status=status.HTTP_201_CREATED)
