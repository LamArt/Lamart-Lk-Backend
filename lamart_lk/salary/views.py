from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse

from authentication.models import ProviderToken
from salary.serializers import SalarySerializer
from salary.utils.story_points import StoryPoints
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
                'rate': serializers.IntegerField(),
                'credit': serializers.IntegerField(),
                'reward': serializers.IntegerField(),
            }
        )},
        summary='Get salary data of user for current month',
        description='Count salary, return story points and another data for current month',
        tags=['salary'],
    )
    def get(self, request):
        try:
            atlassian_tokens = ProviderToken.objects.get(user=request.user, provider='atlassian')
            user_story_points = StoryPoints(atlassian_tokens.refresh_token, request.user)
        except ProviderToken.DoesNotExist:
            return Response('Jira not connected', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('Unauthorized, make jira authentication again', status=status.HTTP_401_UNAUTHORIZED)

        user_salary = Salary.get_salary_data(request.user)
        if user_salary is None:
            return Response('User salary information not found', status=status.HTTP_404_NOT_FOUND)
        story_points = user_story_points.count_at_moment()
        rate = user_salary.rate
        result = {
            'story_points': story_points,
            'salary': rate * story_points,
            'rate': rate,
            'credit': user_salary.credit,
            'reward': user_salary.reward
        }
        return Response(result, status=status.HTTP_200_OK)


class StatisticsStoryPointsView(APIView):
    permissions = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: inline_serializer(
            name='SuccessfulGetStatistics',
            fields={
                'month1': serializers.IntegerField(),
                'month2': serializers.IntegerField(),
                'month3': serializers.IntegerField(),
            }
        )},
        summary='Get story points for statistic graph',
        description='Return story points for last 12 months',
        tags=['salary'],
    )
    def get(self, request):
        try:
            atlassian_tokens = ProviderToken.objects.get(user=request.user, provider='atlassian')
            user_story_points = StoryPoints(atlassian_tokens.refresh_token, request.user)
        except ProviderToken.DoesNotExist:
            return Response('Jira not connected', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('Unauthorized, make jira authentication again', status=status.HTTP_401_UNAUTHORIZED)

        return Response(user_story_points.count_by_months(), status=status.HTTP_200_OK)
