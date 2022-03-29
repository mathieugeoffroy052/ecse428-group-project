from behave import when, then
from django.contrib.auth import get_user_model
from django.urls import reverse
from hamcrest import assert_that, equal_to, none, not_none
from tasklists.models import Task, TaskList

import optional

User = get_user_model()
optional.init_opt_()


@when(u'The user "{email}" attempts to delete the task list "{list_name:opt_?}" with tasks "{task_names}"')
def when_the_user_attempts_to_delete_the_task_list_with_tasks(context, email, list_name, task_names):
    owner = User.objects.filter(email=email).first()
    task_list = TaskList.objects.filter(owner=owner, list_name=list_name).first()
    print(f"List '{list_name}': {task_list}")
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


@when(u'The user "{email}" attempts to delete the task list "{list_name:opt_?}"')
def step_impl(context, email, list_name):
    when_the_user_attempts_to_delete_the_task_list_with_tasks(context, email, list_name, "")


@then(u'The task list "{list_name}" shall be deleted')
def step_impl(context, list_name):
    status_first_digit = context.response.status_code // 100
    assert_that(status_first_digit, equal_to(2))


@then(u'The user "{email}" shall have no task list "{list_name}"')
def step_impl(context, email, list_name):
    owner = User.objects.filter(email=email).first()
    task_lists = TaskList.objects.filter(owner=owner, list_name=list_name)
    print(f"task_lists: {task_lists}")
    if len(task_lists) > 0:
        print(f"task list: {task_lists.first()}, owner: {task_lists.first().owner}, name: {task_lists.first().list_name}")
    assert_that(len(task_lists), equal_to(0))


@then(u'The tasks "{task_names}" will be assigned to no lists')
def step_impl(context, task_names):
    # Split the task names and discard empty names
    task_names_split = [x.strip() for x in task_names.split(",") if x]
    task_objects = [Task.objects.filter(description=name).first() for name in task_names_split]
    for to in task_objects:
        assert_that(to.tasklist, none())


@then(u'No task list shall be deleted')
def step_impl(context):
    if context.response != None:
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))


@then(u'The user "{email}" shall have a list called "{list_name}"')
def step_impl(context, email, list_name):
    owner = User.objects.filter(email=email).first()
    task_list = TaskList.objects.filter(owner=owner, list_name=list_name)
    assert_that(task_list, not_none())


@then(u'The tasks "{task_names}" will be assigned to task list "{list_name}"')
def step_impl(context, task_names, list_name):
    task_list = TaskList.objects.filter(list_name=list_name).first()
    # Split the task names and discard empty names
    task_names_split = [x.strip() for x in task_names.split(",") if x]
    print(f"task_names_split: {task_names_split}")
    task_objects = [Task.objects.filter(description=name).first() for name in task_names_split]
    print(f"task_objects: {task_objects}")
    for to in task_objects:
        assert_that(to.tasklist, equal_to(task_list))
