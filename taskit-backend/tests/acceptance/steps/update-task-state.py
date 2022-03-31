from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, none, is_not
from accounts.models import User
from tasklists.models import Task
from datetime import datetime, timedelta
import json
from common import get_task_status_from_string


@when(
    'The user attempts to update the status of the task "{task_name}" to "{new_state}"'
)
def step_impl(context, task_name, new_state):
    find_task = Task.objects.filter(description=task_name).first()
    print(find_task.state)
    if find_task != None:
        task_id = find_task.id
    else:
        task_id = -1
    try:
        task_status = get_task_status_from_string(new_state)
        task_status_str = str(task_status) if task_status is not None else ""
        status = {"state": task_status_str}

        print(new_state)
        print(status)
        print(task_status)
        print(task_status_str)
        context.response = context.client.put(
            reverse("update_state", kwargs={"pk": task_id}), {"state": task_status_str}
        )
        print(f"Response: {context.response}")
        print(context.response.data)

    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e


@then('the task "{task_name}" shall be updated to "{new_state}"')
def step_impl(context, task_name, new_state):
    task = Task.objects.get(description=task_name)
    task_status = get_task_status_from_string(new_state)
    task_status_str = str(task_status) if task_status is not None else ""
    print(task.state)
    assert_that(
        task.state, equal_to(task_status_str), f"Unable to update to {new_state} state"
    )
    assert_that(context.response.status_code, equal_to(200))
    print(f"Asserting that context.error ({context.error}) is not None.")
    assert_that(context.error, equal_to(None))


@then("no task shall be updated")
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(403))
