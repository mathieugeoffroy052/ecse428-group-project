from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, is_none
from accounts.models import User
from tasklists.models import Task
import json

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()
        print(f"Created user {row['email']}")
        
@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email)
    client = context.client
    client.force_login(user)

@given('All users are logged out')
def step_impl(context):
    client = context.client
    client.logout()

@when(u'The user attempts to update the status of the task "{name}" to "{new_state}"')
def step_impl(context):
    try:
        context.response = context.client.post(reverse('update_state'))
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e

@then(u'the task "{name}" shall be updated to "{new_state}"')
def step_impl(context, description, new_state):
    task = Task.objects.get(description=description)
    new_state_obj = json.loads(new_state)
    assert_that(task.state, equal_to(new_state_obj), 'Unable to update to {new_state} state')
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(None))

@then(u'"{owner}" shall have a task called "{description}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{new_state}"')
def step_impl(context,owner,description,due_date,estimated_duration,weight,new_state):
    task = Task.objects.filter(description=description)
    assert_that(task.owner, equal_to(owner), 'Invalid owner')
    assert_that(task.description, equal_to(description), 'Invalid description')
    assert_that(task.due_date, equal_to(due_date), 'Invalid due date')
    assert_that(task.estimated_duration, equal_to(estimated_duration), 'Invalid estimated duration')
    assert_that(task.weight, equal_to(weight), 'Invalid weight')
    assert_that(task.state, equal_to(new_state), 'Could not update to state {new_state}')


@then(u'The message "Task created succesfully." shall be displayed')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(is_none()))

@then(u'no task shall be updated')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(403))

@then(u'"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{old_state}"')
def step_impl(context,email,name,due_date,estimated_duration,weight,old_state):
    task = Task.objects.filter(name=name)
    assert task.email == email
    assert task.name == name
    assert task.due_date == due_date
    assert task.estimated_duration == estimated_duration
    assert task.weight == weight
    assert task.state == old_state

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
