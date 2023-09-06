from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('exchange_token/', exchange_token, name='exchange_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]