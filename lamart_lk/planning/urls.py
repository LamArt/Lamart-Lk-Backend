from django.urls import path
from .views import *

urlpatterns = [
    path('mail_count/', YandexUnreadMailCountView.as_view(), name='mail_count'),
    path('calendar_events/', YandexCalendarEventsView.as_view(), name='calendar_events'),
    path('jira_issues/', AtlassianJiraIssuesView.as_view(), name='jira_issues')
]