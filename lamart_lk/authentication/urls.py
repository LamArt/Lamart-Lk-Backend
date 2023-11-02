from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('exchange_token/', exchange_provider_token, name='exchange_provider_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_token_jira/', exchange_code_to_token, name='exchange_code_to_token'),
]