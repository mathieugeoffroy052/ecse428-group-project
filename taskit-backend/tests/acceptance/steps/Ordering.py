from django.contrib.auth import get_user_model
from behave import *
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none

User = get_user_model()


@when('The user "{email}" attempts to order their tasks')
def step_impl(context, email):
    try:
        context.response = context.client.get(reverse("task"))
    except BaseException as e:
        context.error = e


@then('The ordering by "Priority" will be "{order}"')
def step_impl(context, order):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    order = order.split(", ")
    tasks = context.response.data
    ordered_tasks = sorted(tasks, key=lambda t: float(t["priority"]), reverse=True)
    assert_that(len(ordered_tasks), equal_to(len(order)))
    actual_task_descriptions = [t["description"] for t in ordered_tasks]
    assert_that(actual_task_descriptions, equal_to(order))


@then('The ordering by "Importance" will be "{order}"')
def step_impl(context, order):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    order = order.split(", ")
    tasks = context.response.data
    ordered_tasks = sorted(tasks, key=lambda t: float(t["importance"]), reverse=True)
    assert_that(len(ordered_tasks), equal_to(len(order)))
    assert_that(len(ordered_tasks), equal_to(len(order)))
    actual_task_descriptions = [t["description"] for t in ordered_tasks]
    assert_that(actual_task_descriptions, equal_to(order))


@then('The ordering by "Urgency" will be "{order}"')
def step_impl(context, order):
    assert_that(context.response, not_none())
    assert_that(context.response.data, not_none())
    order = order.split(", ")
    tasks = context.response.data
    ordered_tasks = sorted(tasks, key=lambda t: float(t["urgency"]), reverse=True)
    assert_that(len(ordered_tasks), equal_to(len(order)))
    assert_that(len(ordered_tasks), equal_to(len(order)))
    actual_task_descriptions = [t["description"] for t in ordered_tasks]
    assert_that(actual_task_descriptions, equal_to(order))
