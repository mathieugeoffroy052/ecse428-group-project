from accounts.models import User
from tasklists.models import Task
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

import optional

optional.init_opt_()

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['username'], row['password'])
        user.save()

@given(u'The following tasks exist')
def step_impl(context):
    for row in context.table:
        task = Task(owner=row['email'], due_datetime = row['due_date'], estimated_duration = row['estimated_duration'], weight = row['weight'])
        task.save()

@given(u'Given "{email:opt_?}" is logged in')
def step_impl(context):
    if request.user.is_authenticated():
    

@when(u'When the user attempts to view all their tasks')
def step_impl(context, username, password):
    context.username = username
    request_data = {
        'email': username if username != None else '',
        'password': password if password != None else ''
    }
    try:
        context.response = context.client.post(reverse('sign_up'), request_data)
        print(context.response)
    except BaseException as e:
        context.error = e

@then(u'a new customer account shall be created')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(None))

@then(u'the account shall have username "{username}" and password "{password}"')
def step_impl(context, username, password):
    user = User.objects.get(email=username)
    assert_that(user.check_password(password), 'Invalid password')

@then(u'no new account shall be created')
def step_impl(context):
    if context.response != None:
        assert_that(context.response.status_code, not(equal_to(201)))

@then(u'an error message "{error}" shall be raised')
def step_impl(context, error):
    e = context.error
    assert_that(e, not_none())
    assert_that(e.message, equal_to(error))