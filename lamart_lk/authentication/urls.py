from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('exchange_token/', ExchangeProviderTokenView.as_view(), name='exchange_provider_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_token_jira/', ExchangeCodeToTokenView.as_view(), name='exchange_code_to_token'),
]
