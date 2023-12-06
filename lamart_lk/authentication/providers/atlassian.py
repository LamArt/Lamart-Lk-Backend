import requests
from datetime import datetime, timedelta

from authentication.providers.base import DataProvider


class AtlassianProvider(DataProvider):
    def __init__(self):
        super().__init__('atlassian')

    def get_token(self, code):
        self.data_params['code'] = code
        self.data_params['grant_type'] = 'authorization_code'
        rq = requests.post(self.oauth_url, data=self.data_params)
        if rq.status_code == 200:
            self.data = rq.json()
        else:
            raise KeyError('not valid authorization code')

    def refresh_token(self, refresh_token):
        self.data_params['grant_type'] = 'refresh_token'
        self.data_params['refresh_token'] = refresh_token
        rq = requests.post(self.oauth_url, data=self.data_params)
        if rq.status_code == 200:
            self.data = rq.json()
        else:
            raise KeyError('not valid refresh token')


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
        atlassian_provider = AtlassianProvider()
        atlassian_provider.refresh_token(self.__refresh_token)
        access = atlassian_provider.data['access_token']
        refresh = atlassian_provider.data['refresh_token']
        self.__access_token = access
        self.headers['Authorization'] = f'Bearer {access}'
        atlassian_provider.save_tokens({'refresh': refresh,
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
