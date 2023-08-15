from .forms import *
from rest_framework import generics
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

class NewReviewFormView(APIView):
    def get(self, request):
        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        context = {
            'full_name': request.user.get_full_name(),
            'is_team_lead': request.user.is_team_leed,
            'gender': request.user.gender,
            'teammates': list(teammates.values('username', 'first_name', 'last_name', 'gender', 'status_level')),
        }
        return Response(context)
    
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