from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, none
import optional


optional.init_opt_()


@when(
    'The user attempts to log in with email address "{email:opt_?}" and password "{password:opt_?}"'
)
def step_when_the_user_attempts_to(context, email, password):
    request_data = {
        "username": email if email != None else "",
        "password": password if password != None else "",
    }
    try:
        context.response = context.client.post(reverse("login"), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e


@then("The user shall be logged in")
def step_impl(context):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.error, none())


@then('The user shall see the task list for "{email}"')
def step_impl(context, email):
    pass


@then("The user shall not be logged in")
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(400))
