from behave import given, then, when
from django.contrib.auth import get_user_model
from django.urls import reverse
from hamcrest import assert_that, equal_to, none, not_none
from tasklists.models import TaskList

import optional

User = get_user_model()
optional.init_opt_()


@when('The user "{email}" attempts to create the task list "{list_name:opt_?}"')
def when_the_user_attempts_to_create_the_task_list(context, email, list_name):
    request_data = {
        "list_name": list_name if list_name is not None else ""
    }
    try:
        print(f"Request data: {request_data}")
        context.response = context.client.post(reverse("create_task_list"), request_data)
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e


@when(u'The user attempts to create the task list of "{email}" called "{list_name}"')
def step_impl(context, email, list_name):
    when_the_user_attempts_to_create_the_task_list(context, email, list_name)


@then(u'the task list "{list_name}" shall exist in the system')
def step_impl(_, list_name):
    task_list = TaskList.objects.filter(list_name=list_name)
    assert_that(task_list, not_none())


@then(u'"{email}" shall have a task list called "{list_name}"')
def step_impl(_, email, list_name):
    owner = User.objects.filter(email=email)
    task_list = TaskList.objects.filter(list_name=list_name, owner=owner)
    assert_that(task_list, not_none())


@then(u'shall not be a list called "{list_name:opt_?}"')
def step_impl(_, list_name):
    task_list = TaskList.objects.filter(list_name=list_name)
    assert_that(task_list, none())


@then(u'no new task list shall be created')
def step_impl(context):
    if context.response != None:
        # Check that status code is 4xx
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))
