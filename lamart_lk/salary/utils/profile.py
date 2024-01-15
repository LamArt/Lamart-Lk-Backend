import requests
from authentication.providers.atlassian import AtlassianProvider


class AtlassianUserProfile:
    ACCESSIBLE_RESOURCES = 'https://api.atlassian.com/oauth/token/accessible-resources'
    BASE_URL = 'https://api.atlassian.com/ex/jira/'

    def __init__(self, refresh, user):
        atlassian_provider = AtlassianProvider()
        atlassian_provider.refresh_token(refresh)
        new_access_token = atlassian_provider.data['access_token']
        new_refresh_token = atlassian_provider.data['refresh_token']
        self.user = user
        self.headers = {'Authorization': f'Bearer {new_access_token}',
                        'Accept': 'application/json'}
        self.search_url = f"{self.BASE_URL}{self.get_cloud_id()}/rest/api/3/"
        self.email = self.get_email()
        atlassian_provider.save_tokens({'refresh': new_refresh_token,
                                        'access': new_access_token}, atlassian_provider.data['expires_in'],
                                       self.user, 'atlassian', 'lamart', self.email)

    def get_cloud_id(self):
        """Get identifier of user to api requests"""

        rq = requests.get(self.ACCESSIBLE_RESOURCES, headers=self.headers)
        if rq.status_code == 200:
            return rq.json()[0]['id']

    def get_email(self):
        """Get user JIRA email"""

        rq = requests.get(f'{self.search_url}/myself', headers=self.headers)
        if rq.status_code == 200:
            data = rq.json()
            return data['emailAddress']

    def take_tasks(self, projects, created_type, email=None):
        """Make request to jira api with JQL, return data of projects"""
        query_of_projects = ' OR '.join([f'project={project}' for project in projects])
        assignee = ''
        if email is not None:
            assignee = f'AND assignee="{email}"'
        jql_query = f'({query_of_projects}) AND created>={created_type} {assignee} AND status IN ("DONE", "НА ПРОВЕРКЕ")'
        params = {
            'jql': jql_query,
            'fields': 'customfield_10129,created',
            'maxResults': 100000,
        }
        rq = requests.get(f'{self.search_url}/search', headers=self.headers, params=params)
        if rq.status_code == 200:
            response_data = rq.json()
            return response_data
