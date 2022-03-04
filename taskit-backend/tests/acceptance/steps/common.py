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

@given('All users are logged out')
def step_impl(context):
    client = context.client
    client.logout()

@then(u'The message "{message}" shall be displayed')
def step_impl(context,message):
    msg = context.response.data
    assert_that(msg, not_none())
    assert_that(message in msg, f'Expected response containing {message} but received {msg}')

@then('The user shall be at the login page')
def step_impl(context):
    pass

@then(u'"{email}" shall have a task called "{name}" with due date "{due_date}", duration "{estimated_duration}", weight "{weight}", and state "Not started"')
# def step_impl(context,email,name,due_date,estimated_duration,weight):
#     task = Task.objects.filter(description=name).first()
#     if(email != "NULL"):
#         assert_that(task.owner, equal_to(User.objects.filter(email=email).first())) 
#     assert_that(task.description, equal_to(name))
#     assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
#     assert_that(str(int(task.estimated_duration.total_seconds())//60), equal_to(estimated_duration))
#     if(weight != "NULL"):
#         assert_that(str(task.weight), equal_to(weight))
def step_impl(context,email,name,due_date,estimated_duration,weight):
    task = Task.objects.filter(description=name).first()
    if(email != "NULL"):
        assert_that(task.owner, equal_to(User.objects.filter(email=email).first())) 
    assert_that(task.description, equal_to(name))
    if due_date != "NULL":
        assert_that(task.due_datetime.strftime("%Y-%m-%d"), equal_to(due_date))
    else:
        assert_that(task.due_datetime, none()) 
    if estimated_duration != "NULL":
        assert_that(str(int(task.estimated_duration.total_seconds())//60), equal_to(estimated_duration))
    else:
        assert_that(task.estimated_duration, none())

    if(weight != "NULL"):
        assert_that(str(task.weight), equal_to(weight))
    