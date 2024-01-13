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

class FormsAboutTeammatesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get self forms about teammates',
        tags=['review']
    )
    def get(self, request):
        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        forms = EmployeeFeedbackForm.objects.filter(created_by=request.user, about__in=teammates)
        serializer = EmployeeFormSerializer(forms, many=True)
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
        if not request.user.is_team_lead:
            return Response("User is not Team lead", status=status.HTTP_403_FORBIDDEN)
        forms = TeamLeadFeedbackForm.objects.filter(created_by=request.user)
        serializer = TeamleadFormSerializer(forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PerfomanceReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get last created perfomance_review',
        tags=['review']
    )
    def get(self, request):
        try:
            last_perfomance_review = PerformanceReview.objects.last()
        except:
            return Response("No perfomance_review found", status=status.HTTP_404_NOT_FOUND)

        serializer = PerformanceReviewSerializer(last_perfomance_review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PerformanceReviewSerializer,
        summary='Create perfomance review',
        tags=['review']
    )
    def post(self, request):
        serializer = PerformanceReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=PerformanceReviewSerializer,
        summary='Update perfomance review',
        tags=['review']
    )
    def patch(self, request):
        try:
            last_perfomance_review = PerformanceReview.objects.last()
        except:
            return Response("No perfomance_review found", status=status.HTTP_404_NOT_FOUND)
        serializer = PerformanceReviewSerializer(last_perfomance_review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="wrong parameters", status=status.HTTP_400_BAD_REQUEST)

