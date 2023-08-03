from django.shortcuts import render

from .forms import *

def new_review_form(request):
    return render(request, 'performance_review/main.html')
