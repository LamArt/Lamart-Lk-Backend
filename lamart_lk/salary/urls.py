from django.urls import path
from .views import *

urlpatterns = [
    path('at_moment/', SalaryView.as_view(), name='salary_at_moment'),
    path('analytics/', AnalyticsStoryPointsView.as_view(), name='analytics')
]
