from accounts.models import User
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, none

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()

@given(u'"{email}" is logged in')
def step_impl(context,email):
    user = User.objects.filter(email=email).first()
    context.client.force_login(user)
    context.client.force_authenticate(user)

@when(u'"{email}" attempts to log out')
def step_impl(context,email):
    try:
        request_data = {
        'user': User.objects.filter(email=email).first()
        }
        context.response = context.client.post(reverse('logout'),request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then(u'The user shall be logged out')
def step_impl(context):
    assert_that(context.response, equal_to(None))
    assert_that(context.error, equal_to(none()))
    
@then('The user shall be at the login page')
def step_impl(context):
    pass