from .models import *
from .serializers import *
from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class NewReviewFormView(APIView):
    """Creating new form for performance review"""

    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
            responses={200: 'ok', 403: 'forbidden'},
    )
    def get(self, request):
        """Gives data about loged in employee and teammates"""

        teammates = User.objects.filter(team=request.user.team).exclude(username=request.user.username)
        context = {
            'full_name': request.user.get_full_name(),
            'is_team_lead': request.user.is_team_lead,
            'gender': request.user.gender,
            'team': request.user.team.name,
            'teammates': list(teammates.values('username', 'first_name', 'last_name', 'gender', 'status_level')),
        }
        return Response(context)
    
    @swagger_auto_schema(
            query_serializer=FormSerializer,
            responses={201: 'form saved successfully', 400: 'bad request', 403: 'forbidden'},
    )
    def post(self, request):
        """Save new form"""
        serialiser = FormSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)