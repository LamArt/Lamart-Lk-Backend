from collections import defaultdict
import requests
from datetime import datetime, timedelta

from salary.utils.profile import AtlassianUserProfile
from salary.utils.projects import EmployeeProjectManager


class SalaryStoryPoints(AtlassianUserProfile, EmployeeProjectManager):
    def __init__(self, refresh_token, user):
        super().__init__(refresh_token, user)
        self.project_manager = EmployeeProjectManager(user)

    current_date = datetime.now()

    def count_story_points_by_projects(self):
        """Counter sp of projects for current month by user"""
        issue_data = self.take_tasks(self.project_manager.get_jira_keys(), 'startOfMonth()')
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

    def get_salary_data(self):
        """Count salary, make result response"""
        story_points = self.count_story_points_by_projects()
        projects_data = self.project_manager.get_projects_data()

        salary_data = {
            'total_salary': 0,
            'projects': {}
        }

        for project_name, project_info in projects_data.items():
            role = project_info['role']
            rate = project_info['rate']
            reward = project_info['reward']
            credit = project_info['credit']

            story_points_for_project = story_points[project_info['jira_key']]
            project_salary = self.calculate_salary(story_points_for_project, rate, role)
            salary_data['total_salary'] += project_salary
            salary_data['projects'][project_name] = {
                'role': role.name,
                'story_points': story_points_for_project,
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
