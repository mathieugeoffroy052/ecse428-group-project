from pickle import NONE
from tasklists.models import Task, TaskList
from accounts.models import User
from behave import *
from datetime import datetime, timedelta
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none, none
import optional
from django.contrib.auth import get_user_model


optional.init_opt_()


@when(
    'The user "{email}" attempts to create the task "{name:opt_?}", with due date "{due_date:opt_?}", duration "{estimated_duration:opt_?}", and weight "{weight:opt_?}"'
)
def step_impl(context, email, name, due_date, estimated_duration, weight):
    request_data = {
        "user": email if email is not None else User.objects.filter(email=email).first,
        "description": name if name is not None else "",
        "due_datetime": due_date if due_date is not None else "",
        "estimated_duration": estimated_duration
        if estimated_duration is not None
        else "",
        "weight": weight if weight is not None else "",
    }
    try:
        # this does not exist yet, might have to change method name later
        context.response = context.client.post(reverse("task"), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e


@when(
    'The user attempts to create the task of "{email:opt_?}" called "{name:opt_?}", due date "{due_date:opt_?}, duration "{estimated_duration:opt_?}", and weight "{weight:opt_?}"'
)
def step_impl(context, email, name, due_date, estimated_duration, weight):
    request_data = {
        "user": email
        if email is not None
        else User.objects.filter(email=email).first(),
        "description": name if name is not None else "",
        "due_datetime": due_date if due_date is not None else "",
        "estimated_duration": estimated_duration
        if estimated_duration is not None
        else "",
        "weight": weight if weight is not None else "",
    }
    try:
        # this does not exist yet, might have to change method name later
        context.response = context.client.post(reverse("task"), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e


@when(
    'The user "{email}" attempts to create the task "{name:opt_?}", with due date "{due_date:opt_?}", duration "{estimated_duration:opt_?}", weight "{weight:opt_?}", and notes "{notes:opt_?}"'
)
def step_impl(context, email, name, due_date, estimated_duration, weight, notes):
    request_data = {
        "user": email if email is not None else User.objects.filter(email=email).first,
        "description": name if name is not None else "",
        "due_datetime": due_date if due_date is not None else "",
        "estimated_duration": estimated_duration
        if estimated_duration is not None
        else "",
        "weight": weight if weight is not None else "",
        "notes": notes if notes is not None else "",
    }
    try:
        context.response = context.client.post(reverse("task"), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e


@when(
    'The user attempts to add the task of "{email}" called "{task_name}" to the list with name "{tasklist_name}"'
)
def step_impl(context, email, task_name, tasklist_name):
    tasklist_id = TaskList.objects.filter(list_name=tasklist_name).first().id
    request_data = {
        "description": task_name,
        "tasklist": tasklist_id,
    }
    try:
        context.response = context.client.post(reverse("task"), request_data)
        print(context.response)
    except Exception as e:
        context.error = e


@then('the task "{name}" shall exist in the system')
def step_impl(context, name):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, none())
    task = Task.objects.filter(description=name).first()
    assert_that(task, not_none())


@then(
    '"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", state "Not started", and notes "{notes}"'
)
def step_impl(context, email, name, due_date, estimated_duration, weight, notes):
    task = Task.objects.filter(description=name).first()
    if email != "NULL":
        assert_that(task.owner.email, equal_to(email))
    assert_that(task.description, equal_to(name))
    assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
    assert_that(
        str(int(task.estimated_duration.total_seconds())), equal_to(estimated_duration)
    )
    if weight != "NULL":
        assert_that(str(task.weight), equal_to(weight))
    else:
        assert_that(task.weight, equal_to(None))
    if notes != "NULL":
        assert_that(str(task.notes), equal_to(notes))
    else:
        assert_that(task.notes, equal_to(""))


@then(
    '"{email}" shall have a task called "{task_name}" in the list with name "{tasklist_name}"'
)
def step_impl(context, email, task_name, tasklist_name):
    user = get_user_model().objects.filter(email=email).first()
    tasklist = TaskList.objects.filter(list_name=tasklist_name).first()
    task = Task.objects.filter(
        owner=user, description=task_name, tasklist=tasklist
    ).first()
    assert_that(task, not_none())


@then(
    '"{email}" shall not have a task called "{task_name}" in the list with name "{tasklist_name}"'
)
def step_impl(context, email, task_name, tasklist_name):
    user = get_user_model().objects.filter(email=email).first()
    tasklist = TaskList.objects.filter(list_name=tasklist_name).first()
    task = Task.objects.filter(
        owner=user, description=task_name, tasklist=tasklist
    ).first()
    assert_that(task, none())


@then('the number of tasks in the system shall be "5"')
def step_impl(context):
    assert len(Task.objects.all()) == 5


@then("no new task shall be created")
def step_impl(context):
    if context.response is not None:
        assert_that(context.response.status_code, equal_to(400))
