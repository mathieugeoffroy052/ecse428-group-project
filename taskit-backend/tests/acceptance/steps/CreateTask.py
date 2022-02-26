from tasklists.models import Task
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none, none
import optional

optional.init_opt_()

@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        #no such thing as create_task, might have to change later
        task = Task.objects.create_task(row['email'], row['task_name'],row['due_date'], row['estimated_duration'], row['weight'], row['state'])
        task.save()

@when(u'The user "{email}" attempts to create the task "{name:opt_?}", with due date "{due_date:opt_?}", duration "{estimated_duration:opt_?}", and weight "{weight:opt_?}"')
def step_impl(context,email,name,due_date,estimated_duration,weight):
    request_data = {
        'email': email if email != None else '',
        'name': name if name != None else '',
        'due_date': due_date if due_date != None else '',
        'estimated_duration': estimated_duration if estimated_duration != None else '',
        'weight': weight if weight != None else ''
    }
    try:
        #this does not exist yet, might have to change method name later
        context.response = context.client.post(reverse('task_list'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@when(u'The user attempts to create the task of "{email:opt_?}" called "{name:opt_?}", due date "{due_date:opt_?}, duration "{estimated_duration:opt_?}", and weight "{weight:opt_?}"')
def step_impl(context,email,name,due_date,estimated_duration,weight):
    request_data = {
        'email': email if email != None else '',
        'name': name if name != None else '',
        'due_date': due_date if due_date != None else '',
        'estimated_duration': estimated_duration if estimated_duration != None else '',
        'weight': weight if weight != None else ''
    }
    try:
        #this does not exist yet, might have to change method name later
        context.response = context.client.post(reverse('task_list'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then(u'the task "{name}" shall exist in the system')
def step_impl(context, name):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(none()))
    task = Task.objects.filter(name=name)
    assert_that(task, not_none())

@then(u'"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "Not started"')
def step_impl(context,email,name,due_date,estimated_duration,weight):
    task = Task.objects.filter(name=name)
    assert task.email == email
    assert task.name == name
    assert task.due_date == due_date
    assert task.estimated_duration == estimated_duration
    assert task.weight == weight

@then(u'the number of tasks in the system shall be "5"')
def step_impl(context):
    assert len(Task.objects) == 5

@then(u'no new task shall be created')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(403))

@then(u'The message "{message}" shall be displayed')
def step_impl(context,message):
    msg = context.response.data
    assert_that(msg, not_none())
    assert_that(message in context.response.data)

@then(u'an error message "{error}" shall be raised')
def step_impl(context, error):
    e = context.error
    if context.error is not None:
        assert_that(e.message, equal_to(error))
    else:
        assert_that(error in context.response.data)