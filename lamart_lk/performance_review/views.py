import datetime
from django.db.models import Avg
from .models import *
from .serializers import *
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse

User = get_user_model()


class TeammatesAPIView(APIView):
    """Get a teammates by user"""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get user teammates',
        tags=['review'],
    )
    def get(self, request):
        """Gives data about loged in employee and teammates"""

        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        context = {
            'teammates': list(teammates.values('id', 'username', 'first_name', 'last_name', 'gender', 'status_level')),
        }
        return Response(context, status=status.HTTP_200_OK)


class EmployeeFormAPIView(APIView):
    """Creating a new employee form"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=EmployeeFormSerializer,
        summary='Get user teammates',
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
        print(user.username)
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
        # hard_skills_rate = (employee_forms.aggregate(Avg('hard_skills_rate')) + teamlead_form.hard_skills_rate) / 2
        # productivity_rate = (employee_forms.aggregate(Avg('productivity_rate')) + teamlead_form.hard_skills_rate) / 2
        # communication_rate = (employee_forms.aggregate(Avg('communication_rate')) + teamlead_form.hard_skills_rate) / 2
        # initiative_rate = (employee_forms.aggregate(Avg('initiative_rate')) + teamlead_form.hard_skills_rate) / 2
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
