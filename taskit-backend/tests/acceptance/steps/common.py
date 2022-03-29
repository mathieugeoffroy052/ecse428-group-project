from behave import given, then
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from tasklists.models import Task
from hamcrest import assert_that, not_none, equal_to, none

User = get_user_model()


def get_task_status_from_string(status_string):
    if status_string == "In progress" or status_string == "IP":
        print("Here's the problem! " + status_string)
        return Task.TaskState.InProgress
    elif status_string == "Not started" or status_string == "NS":
        return Task.TaskState.NotStarted
    elif status_string == "Complete" or status_string == "C":
        return Task.TaskState.Complete
    else:
        return status_string


@given("The following users exist")
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row["email"], row["password"])
        context.user_pwd[row["email"]] = row["password"]
        user.save()


@given('There exists a user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    user = User.objects.create_user(email, password)
    context.user_pwd[email] = password
    user.save()


@given('"{email}" is logged in')
def step_impl(context, email):
    user = User.objects.filter(email=email).first()
    resp = context.client.post(
        reverse("login"),
        {"username": str(user), "password": context.user_pwd[str(user)]},
    )
    context.client.credentials(HTTP_AUTHORIZATION="Token " + resp.data["token"])


@given("The following tasks exist")
def step_impl(context):
    for row in context.table:
        owner = User.objects.filter(email=row["email"]).first()
        if row["due_date"] != "NULL":
            due_date = datetime.fromisoformat(row["due_date"])
        else:
            due_date = None
        if row["estimated_duration"] != "NULL":
            duration = timedelta(seconds=int(row["estimated_duration"]))
        else:
            duration = None
        if "notes" in context.table.headings and row["notes"] != "NULL":
            notes = row["notes"]
        else:
            notes = ""
        task = Task.objects.create_task(
            owner, row["task_name"], due_date, duration, int(row["weight"]), notes
        )
        if "state" in context.table.headings and row["state"] != "NULL":
            task.state = get_task_status_from_string(row["state"])
        task.save()


@given('"{email}" is logged in to their account')
def step_impl(context, email):
    user = User.objects.filter(email=email).first()
    context.client.force_authenticate(user=user)
    print(f"Logging in user {email}")


@given("All users are logged out")
def step_impl(context):
    client = context.client
    client.logout()


@then('The message "{message}" shall be displayed')
def step_impl(context, message):
    msg = context.response.data["success"]
    assert_that(msg, not_none())
    assert_that(message in msg)


@then("The user shall be at the login page")
def step_impl(context):
    pass


@then(
    '"{email}" shall have a task called "{task_name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "{new_state}"'
)
def step_impl(
    context, email, task_name, due_date, estimated_duration, weight, new_state
):
    task = Task.objects.filter(description=task_name).first()
    assert_that(task.owner, equal_to(User.objects.filter(email=email).first()))
    assert_that(task.description, equal_to(task_name))
    if due_date != "NULL":
        assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
    else:
        assert_that(task.due_datetime, none())
    if estimated_duration != "NULL":
        assert_that(
            str(int(task.estimated_duration.total_seconds())),
            equal_to(estimated_duration),
        )
    else:
        assert_that(task.estimated_duration, none())

    if weight != "NULL":
        assert_that(str(task.weight), equal_to(weight))
    else:
        assert_that(task.weight, none())

    task_status = get_task_status_from_string(new_state)
    assert_that(task.state, equal_to(task_status))
