from .forms import *
from .models import *
from .serializers import *
from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response

class NewReviewFormView(APIView):

    #authentication_classes = [authentication.SessionAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        context = {
            'full_name': request.user.get_full_name(),
            'is_team_lead': request.user.is_team_leed,
            'gender': request.user.gender,
            'teammates': list(teammates.values('username', 'first_name', 'last_name', 'gender', 'status_level')),
        }
        return Response(context)
    
    def post(self, request):
        serialiser = FormSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)