from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample

User = get_user_model()


class ProfileData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=inline_serializer(
            name="SuccessfulResponseGetProfile",
            fields={"example": serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                "Example of user profile.",
                value={
                    "first_name": "Иван",
                    "last_name": "Иванов",
                    "surname": 'null',
                    "username": "IvanovIvan@yandex.ru",
                    "phone": "+77786543123",
                    "email": "IvanovIvan@yandex.ru",
                    "avatar_url": "65952/xXXyX0XXxx1uXXssAmcCzcJ4Fk-1",
                    "gender": 'null',
                    "teams": {
                        "Test": {
                            "is_team_lead": 'false',
                            'team_id': '3'
                        },
                        "VMS": {
                            "is_team_lead": 'false',
                            'team_id': '5'
                        },
                        "LK": {
                            "is_team_lead": 'true',
                            'team_id': '1'
                        }
                    },
                    "id": 10

                },
                request_only=False,
                response_only=True,
            ),
        ],
        summary='Get profile data',
        description='Get profile data for logged user',
        tags=['profile'],
    )
    def get(self, request):
        teams = {team.name: {'is_team_lead': team.team_lead == request.user, 'team_id': team.id}
                 for team in request.user.teams.all()}
        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'surname': request.user.surname,
            'username': request.user.username,
            'phone': request.user.phone,
            'email': request.user.email,
            'avatar_url': request.user.avatar_url,
            'gender': request.user.gender,
            'teams': teams,
            'id': request.user.pk
        }
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update profile",
        description="Takes new data and returns updated profile data",
        tags=["profile"],
        request=ProfileSerializer,
        operation_id="Update profile",
    )
    def put(self, request):
        serialiser = ProfileSerializer(request.user, data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
