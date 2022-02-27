from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
import json
from tasklists.models import Task
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

User = get_user_model()

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()

@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        owner = User.objects.filter(email=row['email']).first()
        due_date = datetime.fromisoformat(row['due_date'])
        duration = timedelta(minutes=int(row['estimated_duration']))
        task = Task.objects.create_task(owner, row['task_name'], due_date, duration, row['weight'], row['state'])
        task.save()

@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email).first()
    context.client.force_authenticate(user)

@when(u'The user "{email}" attempts to order their tasks')
def step_impl(context,email):
    try:
        context.response = context.client.get(reverse('task_list'))
        print(f"Response: {context.response}")
        print(f"Response data: {json.loads(json.dumps(context.response.data))}")
        for d in context.response.data:
            print(f"Data: {d}")
    except BaseException as e:
        context.error = e

@then(u'The ordering by "Priority" will be "{order}"')
def step_impl(context,order):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    order = order.split(", ")
    tasks = json.loads(json.dumps(context.response.data))  # wtf
    ordered_tasks = sorted(tasks, key=lambda t: float(t['priority']))
    assert_that(len(ordered_tasks), equal_to(len(order)))
    for x in range(len(ordered_tasks)):
        assert_that(ordered_tasks[x].description, equal_to(order[x]))

@then(u'The ordering by "Importance" will be "{order}"')
def step_impl(context,order):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    order = order.split(", ")
    tasks = json.loads(json.dumps(context.response.data))
    ordered_tasks = sorted(tasks, key=lambda t: float(t['importance']))
    assert_that(len(ordered_tasks), equal_to(len(order)))
    for x in range(len(ordered_tasks)):
        assert_that(ordered_tasks[x].description, equal_to(order[x]))

@then(u'The ordering by "Urgency" will be "{order}"')
def step_impl(context,order):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    order = order.split(", ")
    tasks = json.loads(json.dumps(context.response.data))
    ordered_tasks = sorted(tasks, key=lambda t: float(t['urgency']))
    assert_that(len(ordered_tasks), equal_to(len(order)))
    for x in range(len(ordered_tasks)):
        assert_that(ordered_tasks[x].description, equal_to(order[x]))
