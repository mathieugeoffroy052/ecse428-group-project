from behave import given, then
from hamcrest import assert_that, equal_to
from django.contrib.auth import get_user_model

User = get_user_model()


@given(
    'The tutorial status <has_seen_tutorial> for the user with email "{email}" is "{has_seen_tutorial}"'
)
def step_impl(context, email, has_seen_tutorial):
    user = User.objects.filter(email=email).first()
    user.has_seen_tutorial = True if has_seen_tutorial.lower() == "true" else False
    user.save()


@then("The user shall view the tutorial")
def step_impl(context):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.response.data["has_seen_tutorial"], equal_to(False))


@then("The user shall not view the tutorial")
def step_impl(context):
    pass


@then(
    'The tutorial status <has_seen_tutorial> for the user with email "{email}" shall be "{has_seen_tutorial}"'
)
def step_impl(context, email, has_seen_tutorial):
    user = User.objects.filter(email=email).first()
    has_seen_tutorial = True if has_seen_tutorial.lower() == "true" else False
    assert_that(user.has_seen_tutorial, equal_to(has_seen_tutorial))
