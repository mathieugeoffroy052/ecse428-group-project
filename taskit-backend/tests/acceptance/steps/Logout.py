from accounts.models import User
from behave import *
from django.contrib import auth
from django.urls import reverse

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()

@given(u'"{email}" is logged in')
def step_impl(context,email):
    for user in User.objects.all():
        if user.email == email:
            password = user.password
            client = context.test.client
            client.login(email=email, password=password)

@when(u'"{email}" attempts to log out')
def step_impl(context,email):
    request_data = {
        'email': email if email != None else '',
    }
    try:
        context.response = context.client.post(reverse('logout'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then(u'The user shall be logged out')
def step_impl(context):
    user = auth.get_user(context.client)
    assert not user.is_authenticated
    
@then('The user shall be at the login page')
def step_impl(context):
    pass
      #we need to add that the current that is being viewed is the login page