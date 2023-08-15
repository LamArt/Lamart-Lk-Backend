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

class NewReviewFormView(View):
    #@login_required
    def get(self, request):
        context = {
            'full_name': request.user.get_full_name(),
            'is_team_lead': request.user.is_team_leed,
            'gender': request.user.gender,
            'teammates': list(User.objects.filter(team=request.user.team).values('username', 'first_name', 'last_name', 'gender')),
        }
        return JsonResponse(context)
    
    # def post(self, request):
    #     form = AppForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         form_obj = Form(
    #             created_by=request.user,
    #             like=data['like'],
    #             dislike=data['dislike'],
    #             hard_skills=data['hard_skills'],
    #             productivity=data['productivity'],
    #             communication=data['communication'],
    #             initiative=data['initiative']
    #         )
    #         form_obj.save()
    #         return HttpResponseRedirect('')  # Перенаправить после отправки
        
    #     current_user = request.user
    #     surname = current_user.surname
    #     team = current_user.team.name  
    #     is_team_lead = current_user.is_team_leed
    #     teammates = User.objects.filter(team=current_user.team)

    #     context = {
    #         'surname': surname,
    #         'team': team,
    #         'is_team_lead': is_team_lead,
    #         'teammates': list(teammates.values()),
    #         'form': form
    #     }

    #     return JsonResponse(context)