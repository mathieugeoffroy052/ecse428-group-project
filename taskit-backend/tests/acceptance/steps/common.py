from behave import given, then
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from tasklists.models import Task, TaskList
from hamcrest import assert_that, equal_to, not_none

User = get_user_model()


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
            duration = timedelta(minutes=int(row["estimated_duration"]))
        else:
            duration = None
        if "notes" in row and row["notes"] != "NULL":
            notes = row["notes"]
        else:
            notes = ""
        task = Task.objects.create_task(
            owner, row["task_name"], due_date, duration, int(row["weight"]), notes
        )
        task.save()


@given("The following tasks in the task list exist")
def step_impl(context):
    for row in context.table:
        owner = User.objects.filter(email=row["email"]).first()
        if row["due_date"] != "NULL":
            due_date = datetime.fromisoformat(row["due_date"])
        else:
            due_date = None
        if row["estimated_duration"] != "NULL":
            duration = timedelta(minutes=int(row["estimated_duration"]))
        else:
            duration = None
        if "notes" in row and row["notes"] != "NULL":
            notes = row["notes"]
        else:
            notes = ""
        task_list_name = row["list_name"]
        task_list = TaskList.objects.create_task_list(owner, task_list_name)
        task = Task.objects.create_task(
            owner,
            row["task_name"],
            due_date,
            duration,
            int(row["weight"]),
            notes,
            task_list,
        )
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


@then('The error message "{error}" shall be displayed')
def step_impl(context, error):
    e = context.error
    if context.error is not None:
        assert_that(e.message, equal_to(error))
    else:
        assert_that(
            error in str(context.response.data),
            f"Expected response containing {error} but received {context.response.data}.",
        )


@then("The user shall be at the login page")
def step_impl(context):
    pass
