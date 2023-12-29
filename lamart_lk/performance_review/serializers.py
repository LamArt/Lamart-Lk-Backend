from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import Serializer

from .models import *


class EmployeeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFeedbackForm
        exclude = ['created_by', 'feedback_date']


class TeamleadFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeadFeedbackForm
        exclude = ['created_by', 'feedback_date', 'manager_approve']

