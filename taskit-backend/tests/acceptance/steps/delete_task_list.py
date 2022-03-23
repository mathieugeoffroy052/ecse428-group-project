from behave import when, then
from django.contrib.auth import get_user_model
from django.urls import reverse
from hamcrest import assert_that, equal_to, none
from tasklists.models import Task, TaskList

import optional

User = get_user_model()
optional.init_opt_()


@when(u'The user "{email}" attempts to delete the task list "{list_name:opt_?}"')
def step_impl(context, email, list_name):
    task_list = TaskList.objects.filter(list_name=list_name).first()
    task_list_id = -1 if task_list is None else task_list.id
    request_data = {
        "id": task_list_id
    }
    try:
        print(f"Request data: {request_data}")
        context.response = context.client.delete(reverse("task_list"), request_data)
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e


@then(u'The task list "{list_name}" shall be deleted')
def step_impl(context, list_name):
    status_first_digit = context.response.status_code // 100
    assert_that(status_first_digit, equal_to(2))


@then(u'The user "{email}" shall have no task list "{list_name}"')
def step_impl(context, email, list_name):
    owner = User.objects.filter(email=email).first()
    task_lists = TaskList.objects.filter(owner=owner, list_name=list_name)
    assert_that(task_lists, none())

@then(u'The tasks "{task_names}" will be assigned to no lists')
def step_impl(context, task_names):
    task_objects = [Task.objects.filter(description=name).first() for name in task_names]
    for to in task_objects:
        assert_that(to.list, none())


@then(u'No task list shall be deleted')
def step_impl(context):
    if context.response != None:
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))


@then(u'The user "{email}" shall have a list called "{list_name}"')
def step_impl(context, email, list_name):
    owner = User.objects.filter(email=email).first()
    task_list = TaskList.objects.filter(owner=owner, list_name=list_name)
    assert_that(task_list, none())


@then(u'The tasks "{task_names}" will be assigned to task list "{list_name}"')
def step_impl(context, task_names, list_name):
    task_list = TaskList.objects.filter(list_name=list_name)
    task_objects = [Task.objects.filter(description=name).first() for name in task_names]
    for to in task_objects:
        assert_that(to.list, equal_to(task_list))
