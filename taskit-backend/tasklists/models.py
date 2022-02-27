from django.db import models
from accounts.models import User


class Task(models.Model):
    """
    Model for a user-defined task.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    due_datetime = models.DateTimeField(default=None, blank=True, null=True)
    estimated_duration = models.DurationField(default=None, blank=True, null=True)
    weight = models.IntegerField(default=None, blank=True, null=True)
    class TaskState(models.TextChoices):
        NotStarted = 'NS', 'Not Started'
        InProgress = 'IP', 'In Progress'
        Completed = 'C', 'Completed'
    state = models.CharField(default='None', null=True, choices=TaskState.choices, max_length=2)
