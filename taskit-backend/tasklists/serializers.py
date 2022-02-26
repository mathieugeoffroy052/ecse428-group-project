from rest_framework import serializers
from tasklists.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("description", "due_datetime", "estimated_duration", "weight", "get_urgency", "get_weight", "get_priority")
