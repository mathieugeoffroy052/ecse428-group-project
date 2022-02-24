from accounts.models import User
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, is_none

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()

@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email)
    password = user.password
    client = context.test.client
    client.login(email=email, password=password)

@when(u'"{email}" attempts to log out')
def step_impl(context,email):
    request_data = {
        'email': email if email != None else '',
    }
    try:
        context.response = context.client.post(reverse('logout_request'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then(u'The user shall be logged out')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.error, equal_to(is_none))
    
@then('The user shall be at the login page')
def step_impl(context):
    pass