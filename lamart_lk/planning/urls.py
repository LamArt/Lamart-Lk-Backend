from django.urls import path
from .views import *

urlpatterns = [
    path('mail_count/', GetYandexUnreadMailCountView.as_view(), name='mail_count'),
]