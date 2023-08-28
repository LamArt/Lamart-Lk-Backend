from django.urls import path
from .views import *


urlpatterns = [
    path('exchange_token/', exchange_token, name='exchange_token'),
]