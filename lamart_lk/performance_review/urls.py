from django.urls import path
from .views import *

urlpatterns = [
    path('new/', new_review_form, name='new_review'),
]