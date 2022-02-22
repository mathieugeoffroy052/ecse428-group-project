from accounts.models import User
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none
import optional



optional.init_opt_()


@given('All users are logged out')
def step_impl(context):
    client = context.test.client
    client.logout()
    
@when('The user attempts to log in with email address "{email:opt_?}" and password "{password:opt_?}"')
def step_when_the_user_attempts_to(context,email,password):
    request_data = {
        'email': email if email != None else '',
        'password': password if password != None else ''
    }
    try:
        context.response = context.client.post(reverse('login_request'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then('The user shall be logged in')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.error, equal_to(None))

@then('The user shall see the task list for "{email}"')
def step_impl(context, email):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.error, equal_to(None))

@then('The user shall not be logged in')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, equal_to(401))

@then(u'The error message "{error}" shall be displayed')
def step_impl(context, error):
    e = context.error
    assert_that(e, not_none())
    assert_that(e.message, equal_to(error))