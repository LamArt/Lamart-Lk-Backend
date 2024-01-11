from django.urls import path
from .views import *


urlpatterns = [
    path('teammates/', TeammatesAPIView.as_view(), name='get teammates'),
    path("employee_forms/", EmployeeFormAPIView.as_view(), name='create employee form'),
    path('employee_forms/users/<str:username>/', UserEmployeeFormsAPIView.as_view(), name='get employee form by username'),
    path('teamlead_forms/', TeamleadFeedbackFormAPIView.as_view(), name="create teamlead feedback form"),
    path('teamlead_forms/users/<str:username>/', TeamleadFeedbackFormAPIView.as_view(), name='get teamlead form by username'),
    path('teamlead/forms/created', TeamLeadFormsAPIView.as_view(), name="forms, created by requesting user"),
    path('perfomance_review/', PerfomanceReviewAPIView.as_view(), name="perfomance_review")
]