from rest_framework import serializers
from tasklists.models import Task, TaskList

class TaskListSerializer(serializers.ModelSerializer):
        class Meta:
            model = TaskList
            fields = (
                "list_name",
            )
class TaskSerializer(serializers.ModelSerializer):

    urgency = serializers.SerializerMethodField("get_urgency")

    def get_urgency(self, object):
        return object.get_urgency()[1]

    importance = serializers.SerializerMethodField("get_weight")

    def get_weight(self, object):
        return object.get_weight()

    late = serializers.SerializerMethodField("get_late")

    def get_late(self, object):
        return object.get_urgency()[0]

    priority = serializers.SerializerMethodField("get_priority")

    def get_priority(self, object):
        return object.get_priority()[1]

    class Meta:
        model = Task
        fields = (
            "description",
            "due_datetime",
            "estimated_duration",
            "weight",
            "state",
            "urgency",
            "importance",
            "late",
            "priority",
            "state",
            "notes",
            "id",
        )
