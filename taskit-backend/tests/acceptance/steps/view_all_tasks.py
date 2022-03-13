from accounts.models import User
from tasklists.models import Task
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none
import json
import optional
from datetime import datetime, timedelta, date

optional.init_opt_()


@when("The user attempts to view all their tasks")
def step_impl(context):
    try:
        context.response = context.client.get(reverse("task_list"))
        print(f"Response: {context.response}")
    except BaseException as e:
        print(f"Exception: {e}")
        context.error = e


@then(
    'the view function will return the tasks "{task_names}" (which may or may not be sorted)'
)
def step_impl(context, task_names):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    tasks = context.response.data
    print(tasks)
    actual_tasks = task_names.split(", ")
    assert_that(len(actual_tasks), equal_to(len(tasks)))
