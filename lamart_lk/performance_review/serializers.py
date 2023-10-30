from rest_framework import serializers
from .models import *


class EmployeeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFeedbackForm
        exclude = ['feedback_date']


class TeamleadFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeadFeedbackForm
        exclude = ['feedback_date']

