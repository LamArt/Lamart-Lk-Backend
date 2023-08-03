from .forms import *
from rest_framework import generics
from .models import Form
from .serializers import FormSerializer

class Form_POST_READ(generics.ListCreateAPIView): # чтение всех форм и добавление
     queryset = Form.objects.all()
     serializer_class = FormSerializer

class Form_EDIT(generics.RetrieveUpdateDestroyAPIView): # изменение и удаление
     queryset = Form.objects.all()
     serializer_class = FormSerializer
     #permission_classes = (IsAdminUser)

def new_review_form(request):
    return 0 # отрендерить шаблон с формой


