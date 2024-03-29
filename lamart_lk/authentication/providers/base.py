from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model

from lamart_lk.settings import env
from authentication.models import ProviderToken

User = get_user_model()


class ProviderFactory:
    # all info about providers e.g. urls, auth, organisation domains

    PROVIDERS = {
        'yandex': {
            'oauth_url': 'https://login.yandex.ru/info?format=json',
            'headers': {
                'key': 'Authorization',
                'value': 'OAuth'
            },
            'organisations': {
                'lamart': env('MAIL_DOMAIN')
            }
        },
        'atlassian': {
            'oauth_url': 'https://auth.atlassian.com/oauth/token',
            'headers': {
                'key': 'Authorization',
                'value': 'Bearer'
            },
                'data_params': {
                    'client_id': env('ATTLASSIAN_CLIENT_ID'),
                    'client_secret': env('ATTLASSIAN_CLIENT_SECRET'),
                    'redirect_uri': env('ATTLASSIAN_REDIRECT_URI')
                }
        }
    }
    
    @classmethod
    def get_provider(cls, provider_name):
        provider = cls.PROVIDERS.get(provider_name)
        if not provider:
            raise KeyError('Provider does not exist')
        return provider


class BaseProvider(ProviderFactory):
    def __init__(self, provider):
        try:
            self.provider = self.get_provider(provider)
        except KeyError:
            raise KeyError('provider does not exist')
        self.oauth_url = self.provider['oauth_url']
        self.key = self.provider['headers']['key']
        self.value = self.provider['headers']['value']
        try:
            self.data_params = self.provider['data_params']
        except KeyError:
            self.data_params = None

    @staticmethod
    def save_tokens(tokens, expires_in, user, provider_name, organisation, email=None):
        try:
            user_provider_email = email if email is not None else user.email
            provider_token, created = ProviderToken.objects.update_or_create(
                user=user,
                provider=provider_name,
                organisation=organisation,
                defaults={
                    'access_token': tokens['access'],
                    'refresh_token': tokens['refresh'],
                    'expires_in': expires_in,
                    'user_provider_email': user_provider_email
                }
            )
            return provider_token
        except TypeError:
            raise 'failed to save user tokens'


class AuthProvider(ABC, BaseProvider):
    """contains all methods to work with auth providers"""

    @abstractmethod
    def get_data(self, token):
        pass

    @abstractmethod
    def get_user(self) -> User:
        pass


class DataProvider(ABC, BaseProvider):
    """contains all methods to work with data-taker providers"""

    @abstractmethod
    def get_token(self):
        pass

    @abstractmethod
    def refresh_token(self):
        pass
