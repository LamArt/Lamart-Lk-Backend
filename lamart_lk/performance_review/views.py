from .models import *
from .serializers import *
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model

User = get_user_model()


class NewReviewFormView(APIView):
    """Creating new form for performance review"""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: 'ok', 403: 'forbidden'},
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
        request=FormSerializer,
        responses={201: 'form saved successfully', 400: 'bad request', 403: 'forbidden'},
        tags=['review'],
        summary='Create new form',
        description='Takes params return new saved form'
    )
    def post(self, request):
        serialiser = FormSerializer(data=request.data)
        if not serialiser.is_valid():
            return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serialiser.save(created_by=request.user, about=User.objects.get(username=request.data['about']))
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(f"user {request.data['about']} does not exist", status=status.HTTP_400_BAD_REQUEST)
