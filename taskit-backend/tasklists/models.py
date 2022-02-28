from django.db import models
from django.utils.translation import gettext_lazy
from accounts.models import User

class TaskManager(models.Manager):
    def create_task(self, owner, description, due_datetime, estimated_duration, weight, state):
        task = self.create(owner=owner, description=description, due_datetime=due_datetime, estimated_duration=estimated_duration, weight=weight)
        task.save()
        return task

class Task(models.Model):
    """
    Model for a user-defined task.
    """
    class TaskState(models.TextChoices):
        NotStarted = 'NS', 'Not Started'
        InProgress = 'IP', 'In Progress'
        Completed = 'C', 'Completed'
    state = models.CharField(default='None', null=True, choices=TaskState.choices, max_length=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    due_datetime = models.DateTimeField(default=None, blank=True, null=True)
    estimated_duration = models.DurationField(default=None, blank=True, null=True)
    weight = models.IntegerField(default=None, blank=True, null=True)

    objects = TaskManager()
