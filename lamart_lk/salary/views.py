from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample

from authentication.models import ProviderToken
from salary.utils.salary import SalaryStoryPoints
from salary.utils.projects import EmployeeProjectManager


class SalaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=inline_serializer(
            name="SuccessfulResponseSalary",
            fields={"example": serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                "Example of salary data response.",
                value={"total_salary": 6250,
                       'projects': {
                           "VMS": {
                               "role": "Backend-developer",
                               'story_points': 40,
                               "rate": 650,
                               "salary": 3250,
                               "reward": 5000,
                               "credit": 2000
                           },
                       },
                       },
                request_only=False,
                response_only=True,
            ),
        ],
        summary='Get salary data of user for current month by projects',
        description='Count salary, return story points and another data for current month by projects',
        tags=['salary'],
    )
    def get(self, request):
        try:
            atlassian_tokens = ProviderToken.objects.get(user=request.user, provider='atlassian')
            user_story_points = SalaryStoryPoints(atlassian_tokens.refresh_token, request.user)
        except ProviderToken.DoesNotExist:
            return Response('Jira not connected', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('Unauthorized, make jira authentication again', status=status.HTTP_401_UNAUTHORIZED)

        return Response(user_story_points.get_salary_data(), status=status.HTTP_200_OK)


class StatisticsStoryPointsView(APIView):
    permissions = [permissions.IsAuthenticated]

    @extend_schema(
        responses=inline_serializer(
            name="SuccessfulGetStatistics",
            fields={"example": serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                "Example of statistics data response.",
                value={
                    "December": 20,
                    "November": 15,
                    "October": 10
                },
                request_only=False,
                response_only=True,
            ),
        ],
        summary='Get story points for statistic graph by projects',
        description='Return story points for last 12 months by projects',
        tags=['salary'],
    )
    def get(self, request):
        try:
            atlassian_tokens = ProviderToken.objects.get(user=request.user, provider='atlassian')
            user_story_points = SalaryStoryPoints(atlassian_tokens.refresh_token, request.user)
        except ProviderToken.DoesNotExist:
            return Response('Jira not connected', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('Unauthorized, make jira authentication again', status=status.HTTP_401_UNAUTHORIZED)

        return Response(user_story_points.count_story_points_by_months(), status=status.HTTP_200_OK)
