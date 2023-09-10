from django.urls import path
from .views import *

urlpatterns = [
    path('data/', ProfileData.as_view(), name='data'),
]