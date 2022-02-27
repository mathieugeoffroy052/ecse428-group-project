from rest_framework import serializers
from tasklists.models import Task



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("description", "due_datetime", "estimated_duration", "weight", "state")

