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

#******************* need method name *************
@when(u'The user "{email}" attempts to order their tasks')
def step_impl(context,email):
    request_data = {
        'email': email if email != None else '',
    }
    # try:
        # #this does not exist yet, might have to change method name later
        # context.response = context.client.post(reverse('CreateTask_request'), request_data)
        # print(context.response)
    # except BaseException as e:
    #     context.error = e

@then(u'The ordering by "Priority" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")
    #call view_all tasks 
    # try:
    #     #this does not exist yet, might have to change method name later
    #     context.response = context.client.post(reverse('CreateTask_request'), request_data)
    #     print(context.response)
    # except BaseException as e:
    #     context.error = e


@then(u'The ordering by "Importance" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")
    #call view_all tasks 
    # try:
    #     #this does not exist yet, might have to change method name later
    #     context.response = context.client.post(reverse('CreateTask_request'), request_data)
    #     print(context.response)
    # except BaseException as e:
    #     context.error = e

@then(u'The ordering by "Urgency" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")
    #call view_all tasks 
    # try:
    #     #this does not exist yet, might have to change method name later
    #     context.response = context.client.post(reverse('CreateTask_request'), request_data)
    #     print(context.response)
    # except BaseException as e:
    #     context.error = e