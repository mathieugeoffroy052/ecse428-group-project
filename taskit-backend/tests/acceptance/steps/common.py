from behave import given, then
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from tasklists.models import Task, TaskList
from hamcrest import assert_that, equal_to, none, not_none

User = get_user_model()


@given("The following users exist")
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row["email"], row["password"])
        context.user_pwd[row["email"]] = row["password"]
        user.save()


@given('"{email}" is logged in')
def user_is_logged_in(context, email):
    user = User.objects.filter(email=email).first()
    resp = context.client.post(
        reverse("login"),
        {"username": str(user), "password": context.user_pwd[str(user)]},
    )
    context.client.credentials(HTTP_AUTHORIZATION="Token " + resp.data["token"])


@given('"{email}" is logged in to their account')
def step_impl(context, email):
    user_is_logged_in(context, email)


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
        task_list = TaskList.objects.filter(owner=owner, list_name=row['task_list_name']).first()
        task = Task.objects.create_task(
            owner, row["task_name"], due_date, duration, int(row["weight"]), notes, task_list
        )
        print(f"Created task {task} (name '{task.description}', list '{task.tasklist}')")


@given("All users are logged out")
def step_impl(context):
    client = context.client
    client.logout()


@given("The following lists exist")
def step_impl(context):
    for row in context.table:
        owner = User.objects.filter(email=row["owner"]).first()
        list_name = row["list_name"]
        TaskList.objects.create_task_list(owner, list_name)


@then('The message "{message}" shall be displayed')
def step_impl(context, message):
    msg = context.response.data["success"]
    assert_that(msg, not_none())
    assert_that(message in msg, f"Expected message containing '{message}' but received '{msg}'.")


@then('an error message "{error}" shall be raised')
def step_impl(context, error):
    e = context.error
    if context.error is not None:
        assert_that(e.message, equal_to(error))
    else:
        assert_that(
            error in str(context.response.data),
            f"Expected response containing '{error}' but received {context.response.data}.",
        )


@then("The user shall be at the login page")
def step_impl(context):
    pass


@then(u'the number of lists in the system shall be "{num_lists}"')
def then_the_number_of_lists_in_the_system_shall_be(_, num_lists):
    assert_that(len(TaskList.objects.all()), equal_to(int(num_lists)))


@then(u'the number of task lists in the system shall be "{num_lists}"')
def step_impl(context, num_lists):
    then_the_number_of_lists_in_the_system_shall_be(context, num_lists)
