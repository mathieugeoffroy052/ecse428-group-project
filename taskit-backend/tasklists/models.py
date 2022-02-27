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

    def get_urgency(self) -> (bool, float | None):
        if not self.due_datetime or not self.estimated_duration:
            return (False, None)
        remaining_timedelta = self.due_datetime - datetime.now(timezone.utc)
        remaining_hours = (
            remaining_timedelta.days * 24 + remaining_timedelta.seconds / (60 * 60)
        )  # hours seems to be the most accurate depiction and most used case
        estimated_hours = (
            self.estimated_duration.days * 24
            + self.estimated_duration.seconds / (60 * 60)
        )
        late = remaining_hours < 0
        urgency = (
            -1 * estimated_hours * remaining_hours
            if late
            else estimated_hours / remaining_hours
        )  # the later it is, the more urgent, and the sooner it is due, the more urgent
        return (late, math.atan(urgency) * 2 / math.pi)

    def get_weight(self) -> float | None:
        if not self.weight:
            return None
        return math.atan(self.weight / 100) * 2 / math.pi

    def get_priority(self) -> (bool, float | None):
        urgency = self.get_urgency()
        if not urgency[1] or not self.get_weight():
            return (urgency[0], None)
        return (
            urgency[0],
            urgency[1] * 2 / 3 + self.get_weight(),
        )  # urgency carries more weight than weight
