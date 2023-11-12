from django.urls import path
from .views import *


urlpatterns = [
    path('new/', NewReviewFormView.as_view(), name='new performance review'),
]