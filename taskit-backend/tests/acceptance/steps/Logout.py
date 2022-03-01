import json
from accounts.models import User
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, none
from rest_framework.test import force_authenticate


@when('"{email}" attempts to log out')
def step_impl(context, email):
    try:
        user = User.objects.filter(email=email).first()
        request_data = {"user": user}
        context.response = context.client.post(
            reverse("logout")
            )
        print(context.response)
    except BaseException as e:
        context.error = e


@then("The user shall be logged out")
def step_impl(context):
    user = User.objects.all().first()
    assert_that(context.response.status_code, equal_to(204))
    # assert_that(context.response, equal_to(None))
    assert_that(context.error, none())


@then("The user shall be at the login page")
def step_impl(context):
    pass
