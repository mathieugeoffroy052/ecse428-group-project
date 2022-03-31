from django.contrib.auth import get_user_model
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to

import optional

User = get_user_model()
optional.init_opt_()


@given('there is no existing account with email address "{email}"')
def step_impl(context, email):
    for user in User.objects.all():
        if user.email == email:
            user.delete()


@when(
    'the user provides a new email address "{email:opt_?}" and a password "{password:opt_?}"'
)
def step_impl(context, email, password):
    context.email = email
    request_data = {
        "email": email if email != None else "",
        "password": password if password != None else "",
    }
    try:
        print(f"Request data: {request_data}")
        context.response = context.client.post(reverse("sign_up"), request_data)
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e


@then("a new customer account shall be created")
def step_impl(context):
    assert_that(context.response.status_code, equal_to(201))
    assert_that(context.error, equal_to(None))


@then('the account shall have email address "{email}" and password "{password}"')
def step_impl(context, email, password):
    user = User.objects.get(email=email)
    assert_that(user.check_password(password), "Invalid password")


@then("no new account shall be created")
def step_impl(context):
    print(context.response)
    if context.response != None:
        # Check that status code is 4xx
        status_first_digit = context.response.status_code // 100
        assert_that(status_first_digit, equal_to(4))


@then(
    "there will exist no user with email address {email:opt_?} and a password {password:opt_?}"
)
def step_impl(context, email, password):
    users = User.objects.filter(email=email, password=password)
    assert_that(len(users), equal_to(0))
