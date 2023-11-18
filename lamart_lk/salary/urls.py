from django.urls import path
from .views import *

urlpatterns = [
    path('info/', SalaryView.as_view(), name='salary_info'),
]
