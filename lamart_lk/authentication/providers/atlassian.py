import requests
from datetime import datetime, timedelta
from authentication.providers.base import AtlassianProvider


class AtlassianApiProvider:
    ACCESSIBLE_RESOURCES = 'https://api.atlassian.com/oauth/token/accessible-resources'
    BASE_URL = 'https://api.atlassian.com/ex/jira/'

    def __init__(self, access_token, refresh_token, user):
        self.__access_token = access_token
        self.__refresh_token = refresh_token
        self.user = user
        self.headers = {'Authorization': f'Bearer {self.__access_token}',
                        'Accept': 'application/json'}
        self.search_url = f"{self.BASE_URL}{self.get_cloud_id()}/rest/api/3/"
        self.projects = self.get_projects()

    def refresh_tokens(self):
        atlassian_provider = AtlassianProvider('atlassian')
        atlassian_provider.refresh(self.__refresh_token)
        access = atlassian_provider.data['access_token']
        refresh = atlassian_provider.data['refresh_token']
        self.__access_token = access
        self.headers['Authorization'] = f'Bearer {access}'
        atlassian_provider.save_provider_tokens({'refresh': refresh,
                                                 'access': access}, atlassian_provider.data['expires_in'],
                                                self.user, 'atlassian', 'lamart')

    def get_cloud_id(self):
        """Get identifier of user to api requests"""

        self.refresh_tokens()
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
