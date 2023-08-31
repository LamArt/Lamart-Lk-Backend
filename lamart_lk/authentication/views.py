from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from .providers import Provider
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@authentication_classes([])
@swagger_auto_schema(
    method='post',
    responses={200: 'success', 400: 'wrong token'},
    __name__='exchange_token',
    security=[None],
    )
@api_view(['POST'])
def exchange_token(request, *args, **kwargs):
    """Auth flow: get OAuth token from provider -> exchange it to JWT APItoken"""

    # validating provider
    try:
        provider = Provider(request.data['provider'])
    except KeyError:
        return Response('provider does not exist', status=status.HTTP_400_BAD_REQUEST)
    
    # validating token
    try:
        provider_token = request.data['token']
        provider.get_data(provider_token)
    except KeyError:
        return Response('token is not valid', status=status.HTTP_400_BAD_REQUEST)
    
    # validating organisation and email domain
    try:
        provider.check_organisation(request.data['organisation'])
    except KeyError:
        return Response(f"organisation {request.data['organisation']} is not supperted")
    except ValueError:
        return Response(f"organisation {request.data['organisation']} don't have @{provider.data['default_email'].split('@')[1]} domain")
    
    refresh = RefreshToken.for_user(provider.get_user())
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    } 
    return Response(tokens, status=status.HTTP_200_OK)