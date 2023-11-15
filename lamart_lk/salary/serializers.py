from rest_framework import serializers


class SalarySerializer(serializers.Serializer):
    story_points = serializers.IntegerField()
    salary = serializers.IntegerField()
