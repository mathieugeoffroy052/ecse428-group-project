from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to
from accounts.models import User
from tasklists.models import Task
from datetime import datetime, timedelta
        

@when(u'The user attempts to update the status of the task "{task_name}" to "{new_state}"')
def step_impl(context,task_name,new_state):
    
    find_task = Task.objects.filter(description=task_name).first()

    if find_task != None:
        task_id = find_task.id
    else:
        task_id = -1
    try:
        context.response = context.client.put(reverse("update_state",kwargs={"pk": task_id}), {"state":new_state})
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

@then(u'"{email}" shall have a task called "{task_name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{new_state}"')
def step_impl(context,email,task_name,due_date,estimated_duration,weight,new_state):
    task = Task.objects.filter(description=task_name).first()
    if(email != "NULL"):
        assert_that(task.owner, equal_to(User.objects.filter(email=email).first())) 
    assert_that(task.description, equal_to(email))
    assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
    assert_that(str(int(task.estimated_duration.total_seconds())), equal_to(estimated_duration))
    assert_that(task.state, equal_to(new_state), 'Could not update to state {new_state}')
    if(weight != "NULL"):
        assert_that(str(task.weight), equal_to(weight))

@then(u'no task shall be updated')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(403))

@then(u'The error message "{error}" shall be displayed')
def step_impl(context, error):
    e = context.error
    if context.error is not None:
        assert_that(e.message, equal_to(error))
    else:
        assert_that(error in context.response.data)

@then(u'The user shall be at the login page')
def step_impl(context, error):
    pass
