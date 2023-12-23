from salary.models import UsersProjects


class EmployeeProjectManager:
    def __init__(self, user):
        self.user = user

    @property
    def projects_info(self):
        """Make an instance of UsersProjects"""
        try:
            return UsersProjects.objects.filter(user=self.user)
        except UsersProjects.DoesNotExist:
            return None

    def get_jira_keys(self):
        """Get keys for jira requests"""
        return [project.project.jira_key for project in self.projects_info]

    def get_projects_data(self):
        """Get data of all projects"""
        data = {
            project_data.project.name: {
                'jira_key': project_data.project.jira_key,
                'role': project_data.role,
                'rate': project_data.project.rate,
                'reward': project_data.reward or 0,
                'credit': project_data.credit or 0
            } for project_data in self.projects_info
        }
        return data

    @staticmethod
    def calculate_salary(story_points, rate, role):
        """Calculate salary from salary_formula in Django Admin"""
        try:
            result = eval(role.salary_formula, {'story_points': story_points, 'rate': rate})
            return int(result)
        except TypeError:
            return 0
        except NameError:
            return 0
