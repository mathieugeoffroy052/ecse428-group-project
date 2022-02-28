from accounts.models import User
from tasklists.models import Task
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to
import json
import optional

optional.init_opt_()

@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email)
    password = user.password
    client = context.client
    client.force_login(user)

@when(u'The user attempts to view all their tasks')
def step_impl(context):
    try:
        context.response = context.client.post(reverse('view_all_tasks'))
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e

@then(u'the view function will return the tasks "{task_names}"')
def step_impl(context, task_names):
    tasks = context.response.data
    for actual_task in tasks:
        for expected_task in task_names:
            assert_that(actual_task, equal_to(json.loads(expected_task)), 'Task list invalid')