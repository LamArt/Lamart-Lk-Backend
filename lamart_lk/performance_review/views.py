import datetime
from django.db.models import Avg
from .models import *
from .serializers import *
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from salary.models import TeamMember

User = get_user_model()


class TeammatesAPIView(APIView):
    """Get a teammates by user"""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=inline_serializer(
            name="SuccessfulResponseGetTeammates",
            fields={"example": serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                "Example teammates response.",
                value={"teammates": [
                    {
                        'id': '3',
                        "username": "test_teammate1@test.ru",
                        "first_name": "Иван",
                        "last_name": "Иванов",
                        "gender": "male",
                        "status_level": 'null',
                        "teams__name": "Test project"
                    },
                    {
                        'id': '8',
                        "username": "test_teammate2@test.ru",
                        "first_name": "Андрей",
                        "last_name": "Андреев",
                        "gender": "male",
                        "status_level": 'null',
                        "teams__name": "Test project"
                    }]
                },
                request_only=False,
                response_only=True,
            ),
        ],
        summary='Get teammates data',
        description='Gives data about logged in employee and teammates',
        tags=['review'],
    )
    def get(self, request):
        teams = request.user.teams.all()

        teammates = User.objects.filter(teams__in=teams).exclude(username=request.user.username)
        context = {
            'teammates': list(
                teammates.values('id', 'username', 'first_name', 'last_name', 'gender', 'status_level', 'teams__name')),
        }
        return Response(context, status=status.HTTP_200_OK)


class EmployeeFormAPIView(APIView):
    """Creating a new employee form"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=EmployeeFormSerializer,
        summary='Create employee form',
        tags=['review'],
    )
    def post(self, request):
        """Save new form"""
        serializer = EmployeeFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(created_by=request.user, feedback_date=datetime.datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(f"user {request.data['about']} does not exist", status=status.HTTP_400_BAD_REQUEST)


class UserEmployeeFormsAPIView(APIView):
    """Get employee forms about user"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get employee form by username',
        tags=['review'],
    )
    def get(self, request, username):
        """Get forms by user"""
        user = User.objects.get(username=username)
        employee_forms = EmployeeFeedbackForm.objects.filter(about=user)
        serializer = EmployeeFormSerializer(employee_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamleadFeedbackFormAPIView(APIView):
    """Save team leadForm about user"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get teamlead form by username',
        tags=['review'],
    )
    def get(self, request, username):
        user = User.objects.get(username=username)
        employee_forms = EmployeeFeedbackForm.objects.filter(about=user.id)
        teamlead_form = TeamLeadFeedbackForm.objects.get(about=user)
        serializer = TeamleadFormSerializer(teamlead_form)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=TeamleadFormSerializer,
        summary='Get user teammates',
        tags=['review'],
    )
    def post(self, request):
        """Save new form"""
        serializer = TeamleadFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(created_by=request.user, feedback_date=datetime.datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(f"user {request.data['about']} does not exist", status=status.HTTP_400_BAD_REQUEST)


class TeamLeadFormsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get teamlead forms, created by requested user',
        tags=['review'],
    )
    def get(self, request):
        team_memberships = TeamMember.objects.filter(user=request.user)

        if not team_memberships.exists():
            return Response("User is not linked to any team", status=status.HTTP_403_FORBIDDEN)

        is_team_lead = any(team_member.role.is_team_lead for team_member in team_memberships)

        if not is_team_lead:
            return Response("User is not a team leader", status=status.HTTP_403_FORBIDDEN)

        forms = TeamLeadFeedbackForm.objects.filter(created_by=request.user)
        serializer = TeamleadFormSerializer(forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
