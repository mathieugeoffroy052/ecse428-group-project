from behave import given, then
from hamcrest import assert_that
from django.contrib.auth import get_user_model

User = get_user_model()


@given(
    'The tutorial status <has_seen_tutorial> for the user with email "{email}" is "{has_seen_tutorial}"'
)
def step_impl(context, email, has_seen_tutorial):
    user = User.objects.filter(email=email).first()
    user.has_seen_tutorial = has_seen_tutorial


@then("The user shall view the tutorial")
def step_impl(context):
    pass


@then("The user shall not view the tutorial")
def step_impl(context):
    pass


@then(
    'The tutorial status <has_seen_tutorial> for the user with email "{email}" shall be "{has_seen_tutorial}"'
)
def step_impl(context, email, has_seen_tutorial):
    user = User.objects.filter(email=email).first()
    assert_that(has_seen_tutorial, user.has_seen_tutorial)
