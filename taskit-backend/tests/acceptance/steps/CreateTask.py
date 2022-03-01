from tasklists.models import Task
from accounts.models import User
from behave import *
from datetime import datetime, timedelta
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none, none
import optional


optional.init_opt_()

@when(u'The user "{email}" attempts to create the task "{name:opt_?}", with due date "{due_date:opt_?}", duration "{estimated_duration:opt_?}", and weight "{weight:opt_?}"')
def step_impl(context,email,name,due_date,estimated_duration,weight):
    request_data = {
        'user': email if email != None else User.objects.filter(email=email).first,
        'description': name if name != None else '',
        'due_datetime': due_date if due_date != None else '',
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
        'user': email if email != None else User.objects.filter(email=email).first(),
        'description': name if name != None else '',
        'due_datetime': due_date if due_date != None else '',
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
    assert_that(context.error, none())
    task = Task.objects.filter(description=name).first()
    assert_that(task, not_none())

@then(u'"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "Not started"')
def step_impl(context,email,name,due_date,estimated_duration,weight):
    task = Task.objects.filter(description=name).first()
    if(email != "NULL"):
        assert_that(task.owner, equal_to(User.objects.filter(email=email).first())) 
    assert_that(task.description, equal_to(name))
    assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
    assert_that(str(int(task.estimated_duration.total_seconds())), equal_to(estimated_duration))
    if(weight != "NULL"):
        assert_that(str(task.weight), equal_to(weight))

@then(u'the number of tasks in the system shall be "5"')
def step_impl(context):
    assert len(Task.objects.all()) == 5

@then(u'no new task shall be created')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(400))

