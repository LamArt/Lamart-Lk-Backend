from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework import generics
from .models import Form, User
from .serializers import FormSerializer
from django.shortcuts import render
from .forms import NewReview
from django.http import HttpResponseRedirect, JsonResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View

class Form_POST_READ(generics.ListCreateAPIView): # чтение всех форм и добавление
     queryset = Form.objects.all()
     serializer_class = FormSerializer

class Form_EDIT(generics.RetrieveUpdateDestroyAPIView): # изменение и удаление
     queryset = Form.objects.all()
     serializer_class = FormSerializer
     #permission_classes = (IsAdminUser)

class NewReviewFormView(View):
    def get(self, request):
        current_user = request.user
        surname = current_user.surname
        team = current_user.team.name 
        is_team_lead = current_user.is_team_leed
        teammates = User.objects.filter(team=current_user.team)

        context = {
            'surname': surname,
            'team': team,
            'is_team_lead': is_team_lead,
            'teammates': list(teammates.values()),
        }

        return JsonResponse(context)
    
    def post(self, request):
        form = AppForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form_obj = Form(
                created_by=request.user,
                like=data['like'],
                dislike=data['dislike'],
                hard_skills=data['hard_skills'],
                productivity=data['productivity'],
                communication=data['communication'],
                initiative=data['initiative']
            )
            form_obj.save()
            return HttpResponseRedirect('')  # Перенаправить после отправки
        
        current_user = request.user
        surname = current_user.surname
        team = current_user.team.name  
        is_team_lead = current_user.is_team_leed
        teammates = User.objects.filter(team=current_user.team)

        context = {
            'surname': surname,
            'team': team,
            'is_team_lead': is_team_lead,
            'teammates': list(teammates.values()),
            'form': form
        }

        return JsonResponse(context)
















# @login_required
# def new_review_form(request): # отправляет surname team и т.д., а также после заполнения формы сохроняет в бд
#     current_user = request.user
#     surname = current_user.surname
#     team = current_user.team
#     is_team_lead = current_user.is_team_leed
#     teammates = User.objects.filter(team=current_user.team)

#     if request.method == 'POST':
#         form = AppForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             form_obj = Form(
#                 created_by=request.user,
#                 like=data['like'],
#                 dislike=data['dislike'],
#                 hard_skills=data['hard_skills'],
#                 productivity=data['productivity'],
#                 communication=data['communication'],
#                 initiative=data['initiative']
#             )
#             form_obj.save()
#             return HttpResponseRedirect('')  # перенаправить после отправки
#     else:
#         form = AppForm()

#     context = {
#         'surname': surname,
#         'team': team,
#         'is_team_lead': is_team_lead,
#         'teammates': teammates,
#         'form': form
#     }
    
#     return render(request, main.html, context)