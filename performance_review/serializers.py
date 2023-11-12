from rest_framework import serializers
from .models import Form


class FormInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['created_by', 'about', 'feedback_date']


class TeammateSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    status_level = serializers.CharField()


class TeammatesInfoSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    is_team_lead = serializers.BooleanField()
    gender = serializers.CharField()
    team = serializers.CharField()
    teammates = TeammateSerializer(many=True)


class BadRequestErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(default='Bad request')

class ForbiddenErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(default='Forbidden')
