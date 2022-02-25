from tasklists.models import Task
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none
import optional

optional.init_opt_()

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        #no such thing as create_task, might have to change later
        user = User.objects.create_user(row['email'], row['password'])
        user.save()

@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        #no such thing as create_task, might have to change later
        task = Task.objects.create_task(row['email'], row['task_name'],row['due_date'], row['estimated_duration'], row['weight'], row['state'])
        task.save()

# @given(u' The following types of ordering exist')
# def step_impl(context):
#     for row in context.table:
#         #no such thing as create_task, might have to change later
#         task = Task.objects.create_task(row['email'], row['task_name'],row['due_date'], row['estimated_duration'], row['weight'], row['state'])
#         task.save()


#******************* need method name *************
@when(u'The user "{email}" attempts to order their tasks by "Importance"')
def step_impl(context,email):
    request_data = {
        'email': email if email != None else '',
        'type': 'Importance'
    }
    # try:
        # #this does not exist yet, might have to change method name later
        # context.response = context.client.post(reverse('CreateTask_request'), request_data)
        # print(context.response)
    # except BaseException as e:
    #     context.error = e

#******************* need method name *************
@when(u'The user "{email}" attempts to order their tasks by "Urgency"')
def step_impl(context,email):
    request_data = {
        'email': email if email != None else '',
        'type': 'Urgency'
    }
    # try:
        # #this does not exist yet, might have to change method name later
        # context.response = context.client.post(reverse('CreateTask_request'), request_data)
        # print(context.response)
    # except BaseException as e:
    #     context.error = e

@then(u'the task "{name}" shall exist in the system')
def step_impl(context, name):
    for task in Task.objects.all():
        if task.name == name:
            assert True
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(None))


@then(u'"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "Not started"')
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
        context.response = context.client.post(reverse('CreateTask_request'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then(u'the number of tasks in the system shall be "5"')
def step_impl(context):
    number_of_tasks = 0
    for task in Task.objects.all():
        number_of_tasks += 1
    assert number_of_tasks == 5



@then(u'The message "Task created successfully." shall be displayed')
def step_impl(context):
    msg = context.message
    assert_that(msg, equal_to("Task created successfully"))

@then(u'no new task shall be created')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, not(equal_to(201)))

@then(u'The error message "Log in to edit your tasks." shall be displayed')
def step_impl(context):
    e = context.error
    assert_that(e, not_none())
    assert_that(e.message, equal_to("Login in to edit your tasks."))
