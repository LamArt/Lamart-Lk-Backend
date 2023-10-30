from django.urls import path
from .views import *


urlpatterns = [
    path('teammates/', TeammatesAPIView.as_view(), name='get teammates'),
]