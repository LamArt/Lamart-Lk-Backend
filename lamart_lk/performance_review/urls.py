from django.urls import path
from .views import *

urlpatterns = [
    path('new/', new_review_form, name='new_review'),
    path('v1/', FormAPIList.as_view()),
    path('detail/<int:pk>/', FormAPIDetail.as_view()),
]