from django.db import models
from accounts.models import User

class Task(models.Model):
    '''
    Model for a user-defined task.
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    due_datetime = models.DateTimeField()
    estimated_duration = models.DurationField()
    weight = models.IntegerField()
