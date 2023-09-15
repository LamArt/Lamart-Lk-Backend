from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileData.as_view(), name='data'),
]