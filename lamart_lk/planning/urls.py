from django.urls import path
from .views import *

urlpatterns = [
    path('mail_count/', GetYandexUnreadMailCountView.as_view(), name='mail_count'),
    path('calendar_events/', GetYandexCalendarEventsView.as_view(), name='calendar_events')
]