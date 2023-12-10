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
