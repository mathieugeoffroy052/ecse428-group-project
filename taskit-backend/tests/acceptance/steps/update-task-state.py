from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, none, is_not
from accounts.models import User
from tasklists.models import Task
from datetime import datetime, timedelta
import json


def get_task_status_from_string(status_string):
    if status_string == "In progress" or "IP":
        return Task.TaskState.InProgress
    elif status_string == "Not started" or "NS":
        return Task.TaskState.NotStarted
    elif status_string == "Complete" or "C":
        return Task.TaskState.Complete
    else:
        return status_string


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


@then(
    '"{email}" shall have a task called "{task_name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{new_state}"'
)
def step_impl(
    context, email, task_name, due_date, estimated_duration, weight, new_state
):
    task = Task.objects.filter(description=task_name).first()
    task_status = get_task_status_from_string(new_state)
    task_status_str = str(task_status) if task_status is not None else ""
    assert_that(task.owner, equal_to(User.objects.filter(email=email).first()))
    assert_that(task.description, equal_to(task_name))
    if due_date != "NULL":
        assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
    else:
        assert_that(task.due_datetime, none())
    if estimated_duration != "NULL":
        assert_that(
            str(int(task.estimated_duration.total_seconds()) // 60),
            equal_to(estimated_duration),
        )
    else:
        assert_that(task.estimated_duration, none())

    if weight != "NULL":
        assert_that(str(task.weight), equal_to(weight))
    else:
        assert_that(task.weight, none())
    if context.response.data == "Invalid task state":
        assert_that(
            task.state,
            is_not(equal_to(task_status_str)),
            f"Could not update to state {new_state}",
        )
    assert_that(
        task.state,
        (equal_to(task_status_str)),
        f"Could not update to state {new_state}",
    )


@then("no task shall be updated")
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(403))


@then('The error message "{error}" shall be shown')
def step_impl(context, error):
    first_digit = context.response.status_code // 100
    assert_that(first_digit, equal_to(4))
    assert_that(
        error in json.dumps(context.response.data),
        f"Expected response containing {error} but received {context.response.data}",
   )
