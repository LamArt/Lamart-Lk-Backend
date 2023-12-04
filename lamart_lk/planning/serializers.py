from rest_framework import serializers


class EventDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    url = serializers.CharField()


class MailCountSerializer(serializers.Serializer):
    count = serializers.CharField()


