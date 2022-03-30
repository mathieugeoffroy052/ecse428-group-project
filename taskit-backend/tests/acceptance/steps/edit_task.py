from behave import *
from tasklists.models import Task
from django.urls import reverse
from django.utils.dateparse import parse_duration
from hamcrest import assert_that, equal_to
from common import get_task_status_from_string
import optional

optional.init_opt_()


@when(
    '"{email}" attempts to edit the task name "{previous_task_name}" to have name "{new_task_name:opt_?}"'
)
def step_impl(context, email, previous_task_name, new_task_name):
    task = Task.objects.filter(description=previous_task_name).first()
    request_data = {
        "user": email,
        "id": task.id,
        "description": new_task_name if new_task_name is not None else "",
        "due_datetime": task.due_datetime,
        "estimated_duration": task.estimated_duration,
        "weight": task.weight,
        "state": task.state,
        "notes": task.notes,
    }
    context.response = context.client.put(reverse("task"), request_data)


@when(
    '"{email}" attempts to edit the task name "{task_name}" with due date "{previous_due_date}" to have due date "{new_due_date}"'
)
def step_impl(context, email, task_name, previous_due_date, new_due_date):
    task = Task.objects.filter(description=task_name).first()
    request_data = {
        "user": email,
        "id": task.id,
        "description": task_name,
        "due_datetime": new_due_date,
        "estimated_duration": task.estimated_duration,
        "weight": task.weight,
        "state": task.state,
        "notes": task.notes,
    }
    context.response = context.client.put(reverse("task"), request_data)


@when(
    '"{email}" attempts to edit the task name "{task_name}" with estimated duration "{previous_duration}" to have estimated duration "{new_duration}"'
)
def step_impl(context, email, task_name, previous_duration, new_duration):
    task = Task.objects.filter(description=task_name).first()
    request_data = {
        "user": email,
        "id": task.id,
        "description": task_name,
        "due_datetime": task.due_datetime,
        "estimated_duration": new_duration,
        "weight": task.weight,
        "state": task.state,
        "notes": task.notes,
    }
    context.response = context.client.put(reverse("task"), request_data)


@when(
    '"{email}" attempts to edit the task name "{task_name}" with weight "{previous_weight}" to have new weight "{new_weight}"'
)
def step_impl(context, email, task_name, previous_weight, new_weight):
    task = Task.objects.filter(description=task_name).first()
    request_data = {
        "user": email,
        "id": task.id,
        "description": task_name,
        "due_datetime": task.due_datetime,
        "estimated_duration": task.estimated_duration,
        "weight": new_weight,
        "state": task.state,
        "notes": task.notes,
    }
    context.response = context.client.put(reverse("task"), request_data)


@when(
    '"{email}" attempts to edit the task name "{task_name}" with note "{previous_note:opt_?}" to have new note "{new_note}"'
)
def step_impl(context, email, task_name, previous_note, new_note):
    task = Task.objects.filter(description=task_name).first()
    request_data = {
        "user": email,
        "id": task.id,
        "description": task_name,
        "due_datetime": task.due_datetime,
        "estimated_duration": task.estimated_duration,
        "weight": task.weight,
        "state": task.state,
        "notes": new_note,
    }
    context.response = context.client.put(reverse("task"), request_data)


@then(
    '"{email}" shall not have a task called "{task_name:opt_?}" with due date "{due_date}", duration "{duration}", weight "{weight}", and state "{state}"'
)
def step_impl(context, email, task_name, due_date, duration, weight, state):
    state = get_task_status_from_string(state)
    tasks = Task.objects.filter(
        description=task_name if task_name is not None else "",
        due_datetime=due_date,
        estimated_duration=parse_duration(duration),
        weight=weight,
        state=get_task_status_from_string(state),
    )
    task = tasks.first()
    assert_that(task, equal_to(None))


@then(
    '"{email}" shall not have a task called "{task_name}" with due date "{due_date}", duration "{duration}", weight "{weight}", state "{state}", and note "{note:opt_?}"'
)
def step_impl(context, email, task_name, due_date, duration, weight, state, note):
    state = get_task_status_from_string(state)
    tasks = Task.objects.filter(
        description=task_name,
        due_datetime=due_date,
        estimated_duration=parse_duration(duration),
        weight=weight,
        state=get_task_status_from_string(state),
        notes=note,
    )
    task = tasks.first()
    assert_that(task, equal_to(None))


@then('The number of tasks in the system shall be "{number_of_tasks}"')
def step_impl(context, number_of_tasks):
    assert_that(len(Task.objects.all()), number_of_tasks)
