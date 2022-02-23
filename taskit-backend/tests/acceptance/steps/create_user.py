from accounts.models import User
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

import optional

optional.init_opt_()

@given(u'The following users exist')
def step_impl(context):
    for row in context.table:
        user = User.objects.create_user(row['email'], row['password'])
        user.save()
        print(f"Created user {row['email']}")

@given(u'there is no existing account with email address "{email}"')
def step_impl(context, email):
    for user in User.objects.all():
        if user.email == email:
            user.delete()

@when(u'the user provides a new email address "{email:opt_?}" and a password "{password:opt_?}"')
def step_impl(context, email, password):
    context.email = email
    request_data = {
        'email': email if email != None else '',
        'password': password if password != None else ''
    }
    try:
        context.response = context.client.post(reverse('sign_up'), request_data)
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e

@then(u'a new customer account shall be created')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(None))

@then(u'the account shall have email address "{email}" and password "{password}"')
def step_impl(context, email, password):
    user = User.objects.get(email=email)
    assert_that(user.check_password(password), 'Invalid password')

@then(u'no new account shall be created')
def step_impl(context):
    print(context.response)
    if context.response != None:
        # Check that status code is 4xx
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))

@then(u'an error message "{error}" shall be raised')
def step_impl(context, error):
    e = context.error
    if context.error is not None:
        assert_that(e.message, equal_to(error))
    else:
        assert_that(error in context.response.data)
