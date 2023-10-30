from .models import *
from .serializers import *
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model

User = get_user_model()


class TeammatesAPIView(APIView):
    """Get a teammates by user"""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'ok', 403: 'forbidden'},
    )
    # Получение тиммейтов
    # Форма оценки сотрудниками друг друга получает только тимлид
    # Получение всех форм по данному юзеру
    #
    def get(self, request):
        """Gives data about loged in employee and teammates"""

        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        context = {
            'teammates': list(teammates.values('username', 'first_name', 'last_name', 'gender', 'status_level')),
        }
        return Response(context, status=status.HTTP_200_OK)


class EmployeeFormAPIView(APIView):
    """Creating a new employee form"""

    @swagger_auto_schema(
        query_serializer=EmployeeFormSerializer,
        responses={201: 'form saved successfully', 400: 'bad request', 403: 'forbidden'},
    )
    def post(self, request):
        """Save new form"""
        serializer = EmployeeFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(f"user {request.data['about']} does not exist", status=status.HTTP_400_BAD_REQUEST)


class UserEmployeeFormsAPIView(APIView):
    """Get employee forms about user"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=EmployeeFormSerializer,
        responses={200: 'OK', 400: 'bad request', 403: 'forbidden'},
    )
    def get(self, request):
        """Get forms by user"""
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        employee_forms = EmployeeFeedbackForm.objects.filter(about=user)
        serializer = EmployeeFormSerializer(data=employee_forms, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(employee_forms, status=status.HTTP_200_OK)


class TeamleadFeedbackFormAPIView(APIView):
    """Save team leadForm about user"""

    @swagger_auto_schema(
        query_serializer=EmployeeFormSerializer,
        responses={200: 'OK', 400: 'bad request', 403: 'forbidden'},
    )
    def post(self, request):
        """Save new form"""
        serializer = TeamleadFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(f"user {request.data['about']} does not exist", status=status.HTTP_400_BAD_REQUEST)
