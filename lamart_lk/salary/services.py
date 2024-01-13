from salary.models import TeamMember
from authentication.models import ProviderToken


class UsersProjectsService:
    @staticmethod
    def get_projects_by_user(user):
        return TeamMember.objects.filter(user=user)


class TeamMembersService:
    @staticmethod
    def get_atlassian_teammates_by_project_key(project_key):
        return ProviderToken.objects.filter(
            user__team_memberships__team__jira_key=project_key,
            provider='atlassian'
        )

    @staticmethod
    def get_team_member_data(user_email, project_key):
        return TeamMember.objects.get(
            user__email=user_email,
            team__jira_key=project_key
        )
