from rest_framework import serializers
from .models import Form


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['created_by', 'about', 'feedback_date']
