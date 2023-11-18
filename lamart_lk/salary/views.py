from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse

from authentication.models import ProviderToken
from salary.serializers import SalarySerializer
from authentication.providers.atlassian import AtlassianProvider
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
        summary='Get salary data for user',
        description='Count salary, return story points and another data',
        tags=['salary'],
    )
    def get(self, request):
        try:
            atlassian_token = ProviderToken.objects.get(user=request.user, provider='atlassian').access_token
            atlassian_provider = AtlassianProvider(atlassian_token, request.user)
        except ProviderToken.DoesNotExist:
            return Response('Jira not connected', status=status.HTTP_400_BAD_REQUEST)

        user_salary = Salary.get_salary_data(request.user)
        if user_salary is None:
            return Response('User salary information not found', status=status.HTTP_404_NOT_FOUND)

        story_points = atlassian_provider.count_story_points(user_salary.last_salary_date)
        rate = user_salary.rate
        result = {
            'story_points': story_points,
            'salary': rate * story_points,
            'credit': user_salary.credit,
            'reward': user_salary.reward
        }
        return Response(result, status=status.HTTP_200_OK)

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

        user_salary = Salary.get_salary_data(request.user)
        if user_salary is None:
            return Response('User salary information not found', status=status.HTTP_404_NOT_FOUND)

        serializer = SalarySerializer(user_salary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
