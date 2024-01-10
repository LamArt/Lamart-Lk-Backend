from rest_framework import serializers


class EventDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    url = serializers.CharField()


class EventRRuleSerializer(serializers.Serializer):
    freq = serializers.CharField()
    until = serializers.TimeField(required=False)
    interval = serializers.CharField()
    by_day = serializers.CharField(required=False)
    by_month_day = serializers.CharField(required=False)


class EventCreationSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    rrule = EventRRuleSerializer(required=False)
    create_conference = serializers.BooleanField(required=True)


class MailCountSerializer(serializers.Serializer):
    count = serializers.CharField()


class IssuePrioritySerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.CharField()


class IssueSubTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    priority = IssuePrioritySerializer()
    story_points = serializers.IntegerField()


class IssueDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    priority = IssuePrioritySerializer()
    story_points = serializers.IntegerField()
    subtasks = serializers.ListField(child=IssueSubTaskSerializer())