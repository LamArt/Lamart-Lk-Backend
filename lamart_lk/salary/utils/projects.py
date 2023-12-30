from salary.services import UsersProjectsService


class EmployeeProjectManager:
    def __init__(self, user):
        self.user = user
        self.projects_service = UsersProjectsService()

    @property
    def projects_info(self):
        """Make an instance of UsersProjects"""

        return self.projects_service.get_projects_by_user(self.user)

    def get_jira_keys(self):
        """Get keys for jira requests"""

        return [project.team.jira_key for project in self.projects_info]

    def get_projects_data_for_user(self):
        """Get data of all projects"""

        data = {
            project_data.team.name: {
                'jira_key': project_data.team.jira_key,
                'role': project_data.role,
                'is_team_lead': project_data.team.team_lead,
                'rate': project_data.team.rate,
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
