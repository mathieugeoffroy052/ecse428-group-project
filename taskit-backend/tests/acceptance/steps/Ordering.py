from tasklists.models import Task
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

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

@then(u'Then the ordering will be "{order}"')
def step_impl(context,order):
    request_data = {
        'order': order if order != None else '',
    }
    # try:
    #     #this does not exist yet, might have to change method name later
    #     context.response = context.client.post(reverse('CreateTask_request'), request_data)
    #     print(context.response)
    # except BaseException as e:
    #     context.error = e
