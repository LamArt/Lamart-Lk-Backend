from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiTypes
from django.contrib.auth import get_user_model

from .serializers import *

User = get_user_model()


class NewReviewFormView(APIView):
    """Creating new form for performance review"""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: TeammatesInfoSerializer, 403: ForbiddenErrorSerializer},
        tags=['review'],
        summary='Get logged users',
        description='Gives data about logged in employee and teammates'
    )
    def get(self, request):
        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        context = {
            'full_name': request.user.get_full_name(),
            'is_team_lead': request.user.is_team_lead,
            'gender': request.user.gender,
            'team': request.user.team,
            'teammates': list(teammates.values('username', 'first_name', 'last_name', 'gender', 'status_level')),
        }
        return Response(context)

    @extend_schema(
        request=FormInputSerializer,
        responses={201: OpenApiTypes.OBJECT, 400: BadRequestErrorSerializer, 403: ForbiddenErrorSerializer},
        tags=['review'],
        summary='Create new form',
        description='Takes params return new saved form'
    )
    def post(self, request):
        serializer = FormInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(created_by=request.user, about=User.objects.get(username=request.data['about']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(f"user {request.data['about']} does not exist", status=status.HTTP_400_BAD_REQUEST)
