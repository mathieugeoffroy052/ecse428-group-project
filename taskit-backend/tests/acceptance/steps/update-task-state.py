from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, is_none
from accounts.models import User
from tasklists.models import Task
import json
from datetime import datetime

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()
        print(f"Created user {row['email']}")
        
@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email).first()
    client = context.client
    client.force_login(user)

@given('All users are logged out')
def step_impl(context):
    client = context.client
    client.logout()

@when(u'The user attempts to update the status of the task "{description}" to "{new_state}"')
def step_impl(context,description,new_state):
    request_data = {
        'description': description,
        'new_state' : new_state,
    }
    try:
        context.response = context.client.post(reverse('update_state'))
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e

@then(u'the task "{description}" shall be updated to "{new_state}"')
def step_impl(context, description, new_state):
    task = Task.objects.get(description=description)
    new_state_obj = Task.objects.get(state=new_state)
    assert_that(task.state, equal_to(new_state_obj), 'Unable to update to {new_state} state')
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(None))

@then(u'"{user}" shall have a task called "{description}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{new_state}"')
def step_impl(context,user,description,due_date,estimated_duration,weight,new_state):
    task = Task.objects.filter(description=description)
    user_obj = User.objects.get(email=user)
    due_date_obj = datetime.strptime(due_date, '%y-%m-%d')
    new_state_obj = Task.objects.get(state=new_state)
    assert_that(task.owner, equal_to(user_obj), 'Owner does not match')
    assert_that(task.description, equal_to(description), 'Description does not match')
    assert_that(task.due_date, equal_to(due_date_obj), 'Due date does not match')
    assert_that(task.estimated_duration, equal_to(int(estimated_duration)), 'Duration does not match')
    assert_that(task.weight, equal_to(int(weight)), 'Weight does not match')
    assert_that(task.state, equal_to(new_state_obj), 'Could not update to state {new_state}')


@then(u'The message "Task created succesfully." shall be displayed')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(is_none()))

@then(u'no task shall be updated')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(403))

@then(u'"{user}" shall have a task called "{description}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{old_state}"')
def step_impl(context,user,description,due_date,estimated_duration,weight,old_state):
    task = Task.objects.filter(description=description)
    user_obj = User.objects.get(email=user)
    due_date_obj = datetime.strptime(due_date, '%y-%m-%d')
    old_state_obj = Task.objects.get(state=old_state)
    assert_that(task.owner, equal_to(user_obj), 'User does not match')
    assert_that(task.description, equal_to(description), 'Description does not match')
    assert_that(task.due_date, equal_to(due_date_obj), 'Due date does not match')
    assert_that(task.estimated_duration, equal_to(int(estimated_duration)), 'Duration does not match')
    assert_that(task.weight, equal_to(int(weight)), 'Weight does not match')
    assert_that(task.state, equal_to(old_state_obj), 'Could not update to state {old_state}')
    assert_that(context.response.status_code, equal_to(403))

@then(u'an error message "{error}" shall be displayed')
def step_impl(context, error):
    e = context.error
    if context.error is not None:
        assert_that(e.message, equal_to(error))
    else:
        assert_that(error in context.response.data)

@then(u'user shall be at login page')
def step_impl(context, error):
    pass
