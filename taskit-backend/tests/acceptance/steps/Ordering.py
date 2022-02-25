from black import assert_equivalent
from tasklists.models import Task
from tasklists.views import task_list
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

tasks = []

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

    tasks = task_list(request_data)
    

@then(u'The ordering by "Priority" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")

    try:
        #this does not exist yet, might have to change method name later
        if len(order) != len(tasks):
            raise ValueError('The number of tasks returned does not match the number of user tasks')
        ordered_tasks = []
        current_smallest = None
        for t in tasks:
            for x in range(len(ordered_tasks)):
                if(current_smallest == None):
                    ordered_tasks.append(t)
                    current_smallest = t
                    break
                elif (t.priority >= ordered_tasks[x].priority):
                    ordered_tasks.insert(x,t)
                    break
                elif (t.priority < current_smallest.priority):
                    ordered_tasks.append(t)
                    current_smallest = t
                    break

        for x in range(len(tasks)):
            assert_equivalent(ordered_tasks[x].description, order[x])
    except ValueError as e:
        context.error = e


@then(u'The ordering by "Importance" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")

    try:
        #this does not exist yet, might have to change method name later
        if len(order) != len(tasks):
            raise ValueError('The number of tasks returned does not match the number of user tasks')
        ordered_tasks = []
        current_smallest = None
        for t in tasks:
            for x in range(len(ordered_tasks)):
                if(current_smallest == None):
                    ordered_tasks.append(t)
                    current_smallest = t
                    break
                elif (t.importance >= ordered_tasks[x].importance):
                    ordered_tasks.insert(x,t)
                    break
                elif (t.priority < current_smallest.importance):
                    ordered_tasks.append(t)
                    current_smallest = t
                    break
                    

        for x in range(len(tasks)):
            assert_equivalent(ordered_tasks[x].description, order[x])
    except ValueError as e:
        context.error = e

@then(u'The ordering by "Urgency" will be "{order}"')
def step_impl(context,order):

    order = order.split(", ")

    try:
        #this does not exist yet, might have to change method name later
        if len(order) != len(tasks):
            raise ValueError('The number of tasks returned does not match the number of user tasks')
        ordered_tasks = []
        current_smallest = None
        for t in tasks:
            for x in range(len(ordered_tasks)):
                if(current_smallest == None):
                    ordered_tasks.append(t)
                    current_smallest = t
                    break
                elif (t.priority >= ordered_tasks[x].urgency):
                    ordered_tasks.insert(x,t)
                    break
                elif (t.priority < current_smallest.urgency):
                    ordered_tasks.append(t)
                    current_smallest = t
                    break
                    

        for x in range(len(tasks)):
            assert_equivalent(ordered_tasks[x].description, order[x])
    except ValueError as e:
        context.error = e