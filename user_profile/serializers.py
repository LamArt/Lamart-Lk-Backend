from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone', 'birthday', 'surname'
        ]


class ProfileDataSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    surname = serializers.CharField()
    username = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    avatar_url = serializers.URLField()
    is_team_lead = serializers.BooleanField()
    gender = serializers.CharField()
    team = serializers.CharField()
