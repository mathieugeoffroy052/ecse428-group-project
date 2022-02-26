from black import assert_equivalent
from tasklists.models import Task
from tasklists.views import task_list
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()

@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        task = Task.objects.create_task(row['email'], row['task_name'],row['due_date'], row['estimated_duration'], row['weight'], row['state'])
        task.save()

#******************* need method name *************
@when(u'The user "{email}" attempts to order their tasks')
def step_impl(context,email):
    request_data = {
        'email': email
    }

    context.tasks = task_list(request_data)
    

@then(u'The ordering by "Priority" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")
    ordered_tasks = sorted(context.tasks, key=lambda t: t.priority) 
    for x in range(len(context.tasks)):
        assert_that(ordered_tasks[x].description, equal_to(order[x]))


@then(u'The ordering by "Importance" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")
    ordered_tasks = sorted(context.tasks, key=lambda t: t.importance)
                
    for x in range(len(context.tasks)):
        assert_that(ordered_tasks[x].description, equal_to(order[x]))

@then(u'The ordering by "Urgency" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")
    ordered_tasks = sorted(context.tasks, key=lambda t: t.urgency)             

    for x in range(len(context.tasks)):
        assert_that(ordered_tasks[x].description, equal_to(order[x]))