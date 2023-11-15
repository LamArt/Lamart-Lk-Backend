import requests
from salary.models import Salary

class JiraStoryPoints:
    ACCESSIBLE_RESOURCES = 'https://api.atlassian.com/oauth/token/accessible-resources'
    BASE_URL = 'https://api.atlassian.com/ex/jira/'

    def __init__(self, access_token, user):
        self.__token = access_token
        self.user = user
        self.headers = {'Authorization': f'Bearer {self.__token}',
                        'Accept': 'application/json'}
        self.search_url = f"{self.BASE_URL}{self.get_cloud_id()}/rest/api/3/"

    def get_cloud_id(self):
        """Get identifier of user to api requests"""
        rq = requests.get(self.ACCESSIBLE_RESOURCES, headers=self.headers)
        if rq.status_code == 200:
            return rq.json()[0]['id']

    def get_user_email(self):
        """Get user JIRA email"""
        rq = requests.get(f'{self.search_url}/myself', headers=self.headers)
        if rq.status_code == 200:
            data = rq.json()
            return data['emailAddress']

    def get_projects(self):
        """Make list of projects"""
        rq = requests.get(f'{self.search_url}/project', headers=self.headers)
        if rq.status_code == 200:
            projects_data = rq.json()
            return [project_info['key'] for project_info in projects_data if 'key' in project_info]

    def count_story_points(self):
        """Counter sp of ALL projects with open sprints"""
        projects = ' OR '.join([f'project={project}' for project in self.get_projects()])
        start_date = Salary.objects.get(user=self.user).last_salary_date
        email = self.get_user_email()
        jql_query = f'sprint in openSprints() AND ({projects}) AND updated>={start_date} AND assignee="{email}"'
        params = {
            'jql': jql_query,
            'fields': 'customfield_10016',
            'maxResults': 100000,
        }

        rq = requests.get(f'{self.search_url}/search', headers=self.headers, params=params)
        if rq.status_code == 200:
            response_data = rq.json()
            total_story_points = 0

            for issue in response_data.get('issues', []):
                val = issue['fields'].get('customfield_10016')
                if val is not None:
                    total_story_points += val

            return total_story_points
        else:
            return 0

    def count_salary(self):
        user_rate = Salary.objects.get(user=self.user).rate
        return user_rate

