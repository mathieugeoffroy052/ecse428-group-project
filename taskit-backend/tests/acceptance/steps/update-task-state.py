from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, is_none
from accounts.models import User
from tasklists.models import Task

@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email)
    password = user.password
    client = context.test.client
    client.login(email=email, password=password)

@when(u'The user attempts to update the status of the task "{name}" to "{new_state}"')
def step_impl(context, name, new_state):
    context.name = name
    request_data = {
        'name': name if name != None else '',
        'new_state': new_state if new_state != None else ''
    }
    try:
        context.response = context.client.post(reverse('update_state'), request_data)
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e


@then(u'the task "{name}" shall be updated to "{new_state}"')
def step_impl(context, name, new_state):
    task = Task.objects.get(name=name)
    assert_that(task.state, equal_to(new_state))

@then(u'"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{new_state}"')
def step_impl(context,email,name,due_date,estimated_duration,weight,new_state):
    task = Task.objects.filter(name=name)
    assert task.email == email
    assert task.name == name
    assert task.due_date == due_date
    assert task.estimated_duration == estimated_duration
    assert task.weight == weight
    assert task.state == new_state

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