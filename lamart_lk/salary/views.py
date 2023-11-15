from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema

from authentication.models import ProviderToken
from salary.serializers import SalarySerializer
from salary.atlassianAPI import JiraStoryPoints


class SalaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: SalarySerializer},
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
            return Response('jira not connected', status=status.HTTP_400_BAD_REQUEST)
        story_points = jira.count_story_points()
        rate = jira.count_salary()
        result = {
            'story_points': story_points,
            'salary': rate * story_points,
        }
        return Response(result, status=status.HTTP_200_OK)
