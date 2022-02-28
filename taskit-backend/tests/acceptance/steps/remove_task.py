# Feature: Remove task -> As a user, I wish to be able to remove a task from my task list

import datetime
from django.urls import reverse
from behave import *
from tasklists.models import Task
from hamcrest import assert_that, equal_to, not_none
from accounts.models import User
import optional

optional.init_opt_()

# BACKGROUD
@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        #input filtering for NULL values, which are not a thing in python
        if row["estimated_duration"] != "NULL": 
            est_duration = row["estimated_duration"]
            duration = datetime.timedelta(minutes=int(est_duration))
        else:
            duration = None
        
        due_date = row["due_date"].split("-")
        if due_date != ["NULL"]:
            date = datetime.date(day=int(due_date[2]), month=int(due_date[1]), year=int(due_date[0]))
        else:
            date = None
        #create the tasks
        task = Task.objects.create_task(User.objects.filter(email=row['email']).get(), row['task_name'], date, duration, int(row['weight']), row['state'])
        task.save()
        print(f"Created task named: {row['task_name']}")


# SCENARIO 1 (NORMAL FLOW)
@given(u'"{email}" is logged in to their account')
def step_impl(context, email):
    user = User.objects.filter(email=email).first()
    context.client.force_authenticate(user=user)
    print(f"Logging in user {email}")


@when(u'"{email}" attempts to remove their "{task_name:opt_?}" task due on "{due_date}"')
def step_impl(context, email, task_name, due_date):
    # check the number of tasks that the user has before removing
    context.num_tasks = len(Task.objects.all())
    find_task = Task.objects.filter(description=task_name, due_datetime=due_date).first()
    
    if find_task != None:
        task_id = find_task.id
    else:
        task_id = -1
    
    # attempt to remove task
    try:
        context.response = context.client.delete(
            reverse("task_list"),
            {
                "id": task_id
            }
        )
    except BaseException as e:
        context.error = e
    


@then(u'The task of "{email}" called "{task_name}" shall be removed from the task list')
def step_impl(context, email, task_name):
    # check for task in lists of all tasks
    task = Task.objects.filter(description=task_name).first()
    assert_that(task, equal_to(None))
    
    
@then(u'there shall be 1 less task in the task list')
def step_impl(context):
    assert_that(len(Task.objects.all()), equal_to(context.num_tasks - 1))


# SCENARIO 2 (ERROR FLOW)
@then(u'the system shall report "{error}"')
def step_impl(context, error):
    # check if in context.error, otherwise check data returned by post
    if context.error == error:
        assert_that(context.error, equal_to(error))
    else:
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))
        assert_that(context.response.data["error"], equal_to(error))
        

@then(u'there shall be 0 fewer tasks in the task list')
def step_impl(context):
    assert_that(len(Task.objects.all()), equal_to(context.num_tasks))