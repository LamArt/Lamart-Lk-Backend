from salary.models import UsersProjects


class UsersProjectsService:
    @staticmethod
    def get_projects_by_user(user):
        try:
            return UsersProjects.objects.filter(user=user)
        except UsersProjects.DoesNotExist:
            return None
