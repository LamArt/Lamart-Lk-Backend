import requests
from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model

User = get_user_model()

# all info about providers e.g. urls, auth, organisation domains
PROVIDERS = {
    'yandex': {
        'oauth_url': 'https://login.yandex.ru/info?format=json',
        'headers': {
            'key': 'Authorization',
            'value': 'OAuth'
        },
        'organisations': {
            'lamart': 'yandex',
        }
    },
    'jira': {
        'oauth_url': 'https://auth.atlassian.com/oauth/token',
        'headers': {
            'key': 'Authorization',
            'value': 'Bearer'
        },
        'data_params': {
            'client_id': 'OFe6NSNJiBJypHiGeEMinCsohVPFfXAV',
            'client_secret': 'ATOAfeVYlgQVJPi7CNSkvAtPLvymr6Uyw4foeBjC1-iZorQUFDn7TvO6r_58KArFSn4h4EE5A385',
            'redirect_uri': 'https://localhost/callback'
        }
    }
}


class Provider(ABC):
    """contains all methods to work with social providers"""
    def __init__(self, provider):
        try:
            self.provider = PROVIDERS[provider]
        except KeyError:
            raise KeyError('provider does not exist')
        self.oauth_url = self.provider['oauth_url']
        self.key = self.provider['headers']['key']
        self.value = self.provider['headers']['value']
        try:
            self.data_params = self.provider['data_params']
        except KeyError:
            self.data_params = None

    @abstractmethod
    def get_data(self, token):
        pass

    @abstractmethod
    def get_user(self) -> User:
        pass


class YandexProvider(Provider):
    def get_data(self, token):
        rq = requests.get(url=self.provider['oauth_url'],
                          headers={self.provider['headers']['key']: self.provider['headers']['value'] + token})
        if rq.status_code == 200:
            self.data = rq.json()
            self.token = token
        else:
            raise KeyError('token is not valid')

    def check_organisation(self, organisation):
        email_domain = self.provider['organisations'][organisation]
        if email_domain not in self.data['default_email']:
            raise ValueError('wrong email')

    def get_user(self) -> User:
        """updates and returns user instance if it exists, otherwise creates"""
        if self.provider == PROVIDERS['yandex']:
            new_user = User.objects.filter(username=self.data['default_email']).update_or_create(
                username=self.data['default_email'],
                password=self.token,
                first_name=self.data['first_name'],
                last_name=self.data['last_name'],
                avatar_url=self.data['default_avatar_id'],
                birthday=self.data['birthday'],
                email=self.data['default_email'],
                gender=self.data['sex'],
                phone=self.data['default_phone'],
            )
        return new_user[0]


class JiraProvider(Provider):
    def get_data(self, code):
        self.data_params['code'] = code
        self.data_params['grant_type'] = 'authorization_code'
        rq = requests.post(self.oauth_url, data=self.data_params)
        if rq.status_code == 200:
            data = rq.json()
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')

            return access_token, refresh_token
        else:
            raise KeyError('not valid authorization code')

    def check_organisation(self, organisation):
        pass

    def get_user(self) -> User:
        pass
