from django.urls import path
from .views import *


urlpatterns = [
    path('new/', new_review_form, name='new_review'),
    path('read-app/', Form_POST_READ.as_view()), # по url review/read_app/ чтение всех форм и добавление
    path('edit/<int:pk>/', Form_EDIT.as_view()), # по url review/edit/"id формы"/ изменение и удаление
]