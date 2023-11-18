from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse

from authentication.models import ProviderToken
from salary.serializers import SalarySerializer
from salary.atlassianAPI import JiraStoryPoints
from salary.models import Salary


class SalaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SalarySerializer

    @extend_schema(
        responses={200: inline_serializer(
            name='SuccessfulResponseSalary',
            fields={
                'story_points': serializers.IntegerField(),
                'salary': serializers.IntegerField(),
                'credit': serializers.IntegerField(),
                'reward': serializers.IntegerField(),
            }
        )},
        summary='Count salary by user',
        description='Return all storypoints by user and salary',
        tags=['salary'],
    )
    def get(self, request):
        try:
            user = request.user
            atlassian_token = ProviderToken.objects.get(user=user, provider='atlassian').access_token
            jira = JiraStoryPoints(atlassian_token, user)
        except ProviderToken.DoesNotExist:
            return Response('Jira not connected', status=status.HTTP_400_BAD_REQUEST)
        try:
            story_points = jira.count_story_points()
            user_info = jira.get_user_salary_info()
            if user_info is None:
                return Response('User salary information not found', status=status.HTTP_404_NOT_FOUND)
            rate = user_info.rate
            result = {
                'story_points': story_points,
                'salary': rate * story_points,
                'credit': user_info.credit,
                'reward': user_info.reward
            }
            return Response(result, status=status.HTTP_200_OK)
        except AttributeError:
            return Response('User salary information is not completed')

    @extend_schema(
        responses={
            201: OpenApiResponse(description="Successful update"),
            400: OpenApiResponse(description="Request error"),
            403: OpenApiResponse(description="Forbidden request, only for admins"),
            404: OpenApiResponse(description="User salary not found")
        },
        summary='Update salary info',
        description='Update salary info ONLY BY ADMIN (user stuff_status=True)',
        tags=['salary'],
    )
    def put(self, request):
        if not request.user.is_staff:
            return Response('Forbidden request, only for admins', status=status.HTTP_403_FORBIDDEN)
        try:
            salary_info = Salary.objects.get(user=request.user)
        except Salary.DoesNotExist:
            return Response('User salary not found', status=status.HTTP_404_NOT_FOUND)

        serializer = SalarySerializer(salary_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
