# Feature: Remove task -> As a user, I wish to be able to remove a task from my task list

from django.urls import reverse
from behave import *
from tasklists.models import Task
from hamcrest import assert_that, equal_to, not_none
from accounts.models import User
import optional

optional.init_opt_()

# SCENARIO 1 (NORMAL FLOW)

@when('"{email}" attempts to remove their "{task_name:opt_?}" task due on "{due_date}"')
def step_impl(context, email, task_name, due_date):
    # check the number of tasks that the user has before removing
    context.num_tasks = len(Task.objects.all())
    find_task = Task.objects.filter(
        description=task_name, due_datetime=due_date
    ).first()

    if find_task != None:
        task_id = find_task.id
    else:
        task_id = -1

    # attempt to remove task
    try:
        context.response = context.client.delete(reverse("task_list"), {"id": task_id})
    except BaseException as e:
        context.error = e


@then('The task of "{email}" called "{task_name}" shall be removed from the task list')
def step_impl(context, email, task_name):
    # check for task in lists of all tasks
    task = Task.objects.filter(description=task_name).first()
    assert_that(task, equal_to(None))


@then("there shall be 1 less task in the task list")
def step_impl(context):
    assert_that(len(Task.objects.all()), equal_to(context.num_tasks - 1))


# SCENARIO 2 (ERROR FLOW)
@then('the system shall report "{error}"')
def step_impl(context, error):
    # check if in context.error, otherwise check data returned by post
    if context.error == error:
        assert_that(context.error, equal_to(error))
    else:
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))
        assert_that(context.response.data["error"], equal_to(error))


@then("there shall be 0 fewer tasks in the task list")
def step_impl(context):
    assert_that(len(Task.objects.all()), equal_to(context.num_tasks))
