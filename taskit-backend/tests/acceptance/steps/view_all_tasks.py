from accounts.models import User
from tasklists.models import Task
from accounts.views import login_request
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


