from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiTypes
from django.contrib.auth import get_user_model

from .serializers import *
from performance_review.serializers import ForbiddenErrorSerializer, BadRequestErrorSerializer

User = get_user_model()


class ProfileData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: ProfileDataSerializer, 403: ForbiddenErrorSerializer},
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
        responses={201: OpenApiTypes.OBJECT, 400: BadRequestErrorSerializer, 403: ForbiddenErrorSerializer},
        request=ProfileInputSerializer,
        summary='Update profile',
        description='Takes new data returns updated profile data',
        tags=['profile'],
    )
    def put(self, request):
        serializer = ProfileInputSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
