from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import Serializer

from .models import *


class EmployeeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFeedbackForm
        exclude = ['feedback_date']


class TeamleadFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeadFeedbackForm
        exclude = ['created_by', 'feedback_date', 'manager_approve']

class PerformanceReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceReview
        fields = '__all__'

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


