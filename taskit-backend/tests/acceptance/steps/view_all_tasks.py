from accounts.models import User
from tasklists.models import Task
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to

import optional

optional.init_opt_()

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['username'], row['password'])
        user.save()

@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        task = Task(owner=row['email'], due_datetime = row['due_date'], estimated_duration = row['estimated_duration'], weight = row['weight'])
        task.save()

@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email)
    password = user.password
    client = context.test.client
    client.login(email=email, password=password)

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
    tasks = Task.objects.get(task_names=task_names) 
    assert_that(tasks, equal_to(task_names))