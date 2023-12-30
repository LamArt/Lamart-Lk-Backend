from collections import defaultdict
import requests
from datetime import datetime, timedelta

from salary.utils.profile import AtlassianUserProfile
from salary.utils.projects import EmployeeProjectManager

from salary.services import TeamMembersService


class SalaryStoryPoints(AtlassianUserProfile, EmployeeProjectManager, TeamMembersService):
    def __init__(self, refresh_token, user):
        super().__init__(refresh_token, user)
        self.project_manager = EmployeeProjectManager(user)

    current_date = datetime.now()

    def count_story_points_by_projects(self, project, email=None):
        """Counter sp of projects for current month by user"""

        issue_data = self.take_tasks(project, 'startOfMonth()', email)
        if issue_data is None:
            return {}

        project_points = {}

        for issue in issue_data.get('issues', []):
            key = issue['key'].split('-')[0]
            story_points = issue['fields'].get('customfield_10016')
            if story_points is not None:
                if key not in project_points:
                    project_points[key] = 0
                project_points[key] += int(story_points)
        return project_points

    def count_salary_for_team_leader_by_project(self, project):
        """Count salary for team lead like summ of teammates by project"""

        teammates_data = TeamMembersService.get_atlassian_teammates_by_project_key(project['jira_key'])
        team_lead_salary_data = {'story_points': 0, 'salary': 0}
        for teammate in teammates_data:
            team_member_role = TeamMembersService.get_team_member_data(teammate.user, project['jira_key']).role
            project_sp = self.count_story_points_by_projects([str(project['jira_key'])],
                                                             teammate.user_provider_email)
            if project_sp:
                project_salary = self.calculate_salary(project_sp[project['jira_key']], project['rate'],
                                                       team_member_role)
                team_lead_salary_data['salary'] += project_salary
                team_lead_salary_data['story_points'] += project_sp[project['jira_key']]
        return team_lead_salary_data

    def get_salary_data(self):
        """Get salary, make result response"""

        projects_data = self.project_manager.get_projects_data_for_user()
        salary_data = {
            'total_salary': 0,
            'projects': {}
        }

        for project_name, project_info in projects_data.items():
            role = project_info['role']
            rate = project_info['rate']
            reward = project_info['reward']
            credit = project_info['credit']

            is_team_lead = project_info.get('is_team_lead', False)

            if is_team_lead == self.user:
                salary_team_lead = self.count_salary_for_team_leader_by_project(project_info)
                project_salary = salary_team_lead['salary']
            else:
                story_points = self.count_story_points_by_projects(self.project_manager.get_jira_keys(), self.email)
                story_points_for_project = story_points.get(project_info.get('jira_key'), 0)
                project_salary = self.calculate_salary(story_points_for_project, rate, role)

            salary_data['total_salary'] += project_salary + reward - credit
            salary_data['projects'][project_name] = {
                'role': role.name,
                'story_points': salary_team_lead[
                    'story_points'] if is_team_lead == self.user else story_points_for_project,
                'rate': rate,
                'salary': project_salary,
                'reward': reward,
                'credit': credit,
            }

        return salary_data


def count_story_points_by_months(self):
    """Counter sp for the last 12 months"""

    time_delta = 10 * 4
    issue_data = self.take_tasks(self.project_manager.get_jira_keys(), 'startOfMonth(-12M)')
    time_data = defaultdict(int)
    if issue_data is None:
        return {}
    for issue in issue_data.get('issues', []):
        issue_date = datetime.strptime(issue['fields']['created'][:-6], "%Y-%m-%dT%H:%M:%S.%f")

        for i in range(time_delta):
            start_time = self.current_date.replace(day=1) - timedelta(weeks=i * 4)
            end_time = (start_time.replace(day=1) +
                        timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0) - timedelta(seconds=1)

            if start_time <= issue_date <= end_time:
                time_name = start_time.strftime('%B')
                time_data[time_name] += issue['fields']['customfield_10016']

    result = dict(sorted(time_data.items()))
    return result
