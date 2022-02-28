from accounts.models import User
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, none

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
    user = User.objects.all().first()
    #assert_that(context.response.status_code, equal_to(302))
    #assert_that(context.response, equal_to(None))
    assert_that(context.error, equal_to(none()))
    
@then('The user shall be at the login page')
def step_impl(context):
    pass