from django.urls import path
from .views import *

urlpatterns = [
    path('count/', SalaryView.as_view(), name='exchange_provider_token'),
]
