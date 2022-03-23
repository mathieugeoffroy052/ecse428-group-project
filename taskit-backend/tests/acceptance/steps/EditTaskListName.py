from asyncio import Task
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none


@given(u'The following task lists exist')
def step_impl(context):
    for row in context.table:
        task_list = TaskList.objects.create_task_list(row["email"], row["task_list_name"])
        tasklist.save()


@given(u'The following tasks in the task list exist')
def step_impl(context):
    for row in context.table:
        task = TaskList.objects.create_task(row["email"], row["task_list_name"], row["task_names"])
        task.save()

@when(u'The user "{email}" attempts to edit the task list name "{task_list_name}" to "{new_task_list_name}')
def step_impl(context):
    raise NotImplementedError(u'STEP: When The user "obi-wan.kenobi@gar.gov" attempts to edit the task list name "Training" to "Jedi Training"')


@then(u'the user "{email}" shall have a task list named "{new_task_list_name}"')
def step_impl(context, new_task_list_name):
    owner = User.objects.filter(email=email)
    task_list = TaskList.objects.filter(task_list_name=task_list_name)
    assert_that(new_task_list_name, not_none)

@then(u'"{new_task_list_name}" shall include "{task_names}"')
def step_impl(context, new_task_list_name, task_names):
   task_list = TaskList.objects.filter(task_list_name=new_task_list_name)
   task = Task.objects.filter(task_names=task_names)
   assert_that(task_names, not_none())