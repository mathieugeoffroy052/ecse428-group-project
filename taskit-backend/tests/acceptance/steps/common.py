from behave import given, then
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from tasklists.models import Task
from hamcrest import assert_that, not_none, equal_to, none

User = get_user_model()


@given("The following users exist")
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row["email"], row["password"])
        user.save()


@given('"{email}" is logged in')
def step_impl(context, email):
    user = User.objects.filter(email=email).first()
    context.client.force_authenticate(user)


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
        task = Task.objects.create_task(
            owner,
            row["task_name"],
            due_date,
            duration,
            int(row["weight"]),
            row["state"],
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


@then('The error message "{message}" shall be displayed')
def step_impl(context, message):
    msg = context.response.data
    assert_that(msg, not_none())
    assert_that(
        message in msg, f"Expected response containing {message} but received {msg}"
    )

# @then('The message "{message}" shall be displayed')
# def step_impl(context, message):
#     msg = context.response.data
#     assert_that(msg, not_none())
#     assert_that(
#         message in msg, f"Expected response containing {message} but received {msg}"
#     )

@then('The message "{message}" shall be displayed')
def step_impl(context, message):
    msg = context.response.data["success"]
    assert_that(msg, not_none())
    assert_that(message in msg)


@then("The user shall be at the login page")
def step_impl(context):
    pass
