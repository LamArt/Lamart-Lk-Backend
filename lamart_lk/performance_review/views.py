from .forms import *
from rest_framework import generics

from .models import Form
from .serializers import FormSerializer

class FormAPIList(generics.ListCreateAPIView):
     queryset = Form.objects.all()
     serializer_class = FormSerializer
class FormAPIDetail(generics.RetrieveUpdateDestroyAPIView):
     queryset = Form.objects.all()
     serializer_class = FormSerializer
def new_review_form(request):
    return 0 # отрендерить шаблон с формой
