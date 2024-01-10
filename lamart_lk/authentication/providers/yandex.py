import requests
from django.contrib.auth import get_user_model

from lamart_lk.settings import DEBUG
from authentication.providers.base import AuthProvider

User = get_user_model()


class YandexProvider(AuthProvider):
    def __init__(self):
        super().__init__('yandex')

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
        if DEBUG:
            return
        if email_domain not in self.data['default_email']:
            raise ValueError('wrong email')

    def get_user(self) -> User:
        """updates and returns user instance if it exists, otherwise creates"""

        try:
            new_user = User.objects.filter(username=self.data['default_email']).update_or_create(
                username=self.data['default_email'],
                password=self.token,
                first_name=self.data['first_name'],
                last_name=self.data['last_name'],
                avatar_url=self.data['default_avatar_id'],
                birthday=self.data['birthday'],
                email=self.data['default_email'],
                gender=self.data['sex'],
                phone=self.data['default_phone']['number'],
            )
            return new_user[0]
        except TypeError:
            new_user = User.objects.filter(username=self.data['default_email']).update_or_create(
                username=self.data['default_email'],
                password=self.token,
                first_name=self.data['first_name'],
                last_name=self.data['last_name'],
                avatar_url=self.data['default_avatar_id'],
                birthday=self.data['birthday'],
                email=self.data['default_email'],
                gender=self.data['sex'],
                phone=self.data['default_phone']
            )
            return new_user[0]
        except KeyError:
            raise 'error in getting user'
