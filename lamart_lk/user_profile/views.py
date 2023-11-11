from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: 'ok', 403: 'forbidden'},
        summary='Get profile',
        description='Gives logged user profile data',
        tags=['profile'],
    )
    def get(self, request):
        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'surname': request.user.surname,
            'username': request.user.username,
            'phone': request.user.phone,
            'email': request.user.email,
            'avatar_url': request.user.avatar_url,
            'is_team_lead': request.user.is_team_lead,
            'gender': request.user.gender,
            'team': request.user.team,
        }
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={201: 'created', 400: 'bad request', 403: 'forbidden'},
        request=ProfileSerializer,
        summary='Update profile',
        description='Takes new data returns updated profile data',
        tags=['profile'],
    )
    def put(self, request):
        serialiser = ProfileSerializer(request.user, data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
