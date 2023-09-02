import requests
from .models import ProviderToken
from performance_review.models import User

PROVIDERS_LIST = {
    'yandex': {
        'oauth_url': 'https://login.yandex.ru/info?format=json',
        'headers': {
            'key': 'Authorization',
            'value': 'OAuth'
        },
        'organisations': {
            'lamart': 'lamart.site'
        }
    }
}
class Provider():
    """contains all methods to work with social providers"""

    provider = {} # provider from PROVIDERS_LIST

    def __init__(self, provider):
        try:
            self.provider = PROVIDERS_LIST[provider]
        except KeyError:
            raise KeyError('providor does not exist')
        
        self.oauth_url = self.provider['oauth_url']
        self.key = self.provider['headers']['key']
        self.value = self.provider['headers']['value']

    def get_data(self, token):
        """takes and saves data from provider if given token is valid"""
        rq = requests.get(url=self.provider['oauth_url'], headers={self.provider['headers']['key']: self.provider['headers']['value']+token})
        if rq.status_code == 200:
            self.data = rq.json()
            self.token = token
        else:
            raise KeyError('token is not valid')

    def check_organisation(self, organisation):
        emsil_domain = self.provider['organisations'][organisation]
        if emsil_domain not in self.data['default_email']:
            raise ValueError('wrong email')
    
    def get_user(self)-> User:
        """updates and returns user instance if it exists, otherwise creates"""

        try:
            user = User.objects.get(username=self.data['default_email'])
            User.objects.filter(id = user.pk).update(
                password = self.token,
                first_name = self.data['first_name'],
                last_name = self.data['last_name'],
                avatar_url = self.data['default_avatar_id'],
                birthday = self.data['birthday'],
                email = self.data['default_email'],
                gender = self.data['sex'],
                phone = self.data['default_phone'],
            )
            return user
        except User.DoesNotExist:
            new_user = User.objects.create(
                username = self.data['default_email'],
                password = self.token,
                first_name = self.data['first_name'],
                last_name = self.data['last_name'],
                avatar_url = self.data['default_avatar_id'],
                birthday = self.data['birthday'],
                email = self.data['default_email'],
                gender = self.data['sex'],
                phone = self.data['default_phone'],
            )
            return new_user