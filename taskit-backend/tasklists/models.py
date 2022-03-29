from django.db import models
from django.utils.translation import gettext_lazy
from accounts.models import User
from datetime import datetime, timedelta, date, timezone
import math


class TaskListManager(models.Manager):
    def create_task_list(self, owner, list_name):
        task_list = self.create(owner=owner, list_name=list_name)
        task_list.save()
        return task_list


class TaskList(models.Model):
    """
    Model for a user-defined task list.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=35)
    objects = TaskListManager()

    # Prevent duplicate list names for a given user
    class Meta:
        unique_together = (
            "owner",
            "list_name",
        )


class TaskManager(models.Manager):
    def create_task(
        self,
        owner,
        description,
        due_datetime,
        estimated_duration,
        weight,
        notes="",
        tasklist=None,
    ):
        task = self.create(
            owner=owner,
            tasklist=tasklist,
            description=description,
            due_datetime=due_datetime,
            estimated_duration=estimated_duration,
            weight=weight,
            notes=notes,
        )
        task.save()
        return task


class Task(models.Model):
    """
    Model for a user-defined task.
    """

    class TaskState(models.TextChoices):
        NotStarted = "NS", gettext_lazy("Not started")
        InProgress = "IP", gettext_lazy("In progress")
        Complete = "C", gettext_lazy("Complete")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tasklist = models.ForeignKey(
        TaskList, blank=True, null=True, on_delete=models.SET_NULL
    )
    description = models.CharField(max_length=200)
    due_datetime = models.DateTimeField(default=None, blank=True, null=True)
    estimated_duration = models.DurationField(default=None, blank=True, null=True)
    weight = models.IntegerField(default=None, blank=True, null=True)
    state = models.CharField(
        default=TaskState.NotStarted,
        null=False,
        blank=False,
        choices=TaskState.choices,
        max_length=2,
    )
    notes = models.CharField(default="", blank=True, max_length=200)
    objects = TaskManager()

    def get_urgency(self):
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

    def get_weight(self):
        if not self.weight:
            return None
        return math.atan(self.weight / 100) * 2 / math.pi

    def get_priority(self):
        urgency = self.get_urgency()
        if not urgency[1] or not self.get_weight():
            return (urgency[0], None)
        return (
            urgency[0],
            urgency[1] * 2 / 3 + self.get_weight(),
        )  # Importance is weighted more heavily than urgency
