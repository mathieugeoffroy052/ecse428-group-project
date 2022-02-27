from rest_framework import serializers
from tasklists.models import Task
<<<<<<< HEAD


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("description", "due_datetime", "estimated_duration", "weight")
=======
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("description", "due_datetime", "estimated_duration", "weight", "state")
>>>>>>> a5a6116548feb3e31b61ce6770f28feff790e048
