from django.db import models
from accounts.models import User
from datetime import datetime, timedelta, date, timezone
import math


class Task(models.Model):
    """
    Model for a user-defined task.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    due_datetime = models.DateTimeField(default=None, blank=True, null=True)
    estimated_duration = models.DurationField(default=None, blank=True, null=True)
    weight = models.IntegerField(default=None, blank=True, null=True)

    def get_urgency(self) -> (bool, float):
        remaining_timedelta = self.due_datetime - datetime.now(timezone.utc)
        remaining_hours = remaining_timedelta.days * 24 + remaining_timedelta.seconds / (60 * 60) # hours seems to be the most accurate depiction and most used case
        estimated_hours = self.estimated_duration.days * 24 + self.estimated_duration.seconds / (60 * 60)
        late = remaining_hours < 0
        urgency = -1 * estimated_hours * remaining_hours if late else estimated_hours / remaining_hours # the later it is, the more urgent, and the sooner it is due, the more urgent
        return (late, math.atan(urgency) * 2/math.pi)

    def get_weight(self) -> float:
        return math.atan(self.weight) * 2/math.pi

    def get_importance(self) -> (bool, float):
        urgency = self.get_urgency()
        return (urgency[0], urgency[1] + self.get_weight() * 2/3) # urgency carries more weight than weight
