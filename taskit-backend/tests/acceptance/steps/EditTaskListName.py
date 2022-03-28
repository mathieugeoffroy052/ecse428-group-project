from datetime import datetime, timedelta
from behave import given, then, when
from django.urls import reverse
from hamcrest import assert_that, equal_to, not_none
from tasklists.models import Task, TaskList, TaskListManager, TaskManager
from django.contrib.auth import get_user_model

User = get_user_model()

@given("The following task lists exist")
def step_impl(context):
    for row in context.table:
        owner = User.objects.filter(email=row["email"]).first()
        if row["list_name"] != "NULL":
            task_list_name = row["list_name"]
        else: 
            task_list_name = ""
        task_list = TaskList.objects.create_task_list(owner, task_list_name)
        task_list.save()


@given("The following tasks in the task list exist")
def step_impl(context):
    for row in context.table:
        owner = User.objects.filter(email=row["email"]).first()
        if row["due_date"] != "NULL":
            due_date = datetime.fromisoformat(row["due_date"])
        else:
            due_date = None
        if row["estimated_duration"] != "NULL":
            duration = timedelta(minutes=int(row["estimated_duration"]))
        else:
            duration = None
        if "notes" in row and row["notes"] != "NULL":
            notes = row["notes"]
        else:
            notes = ""
        if row["list_name"] != "NULL":
            task_list_name = row["list_name"]
        else: 
            task_list_name = ""
        task_list = TaskList.objects.create_task_list(owner, task_list_name)
        task = Task.objects.create_task(
            owner, row["task_name"], due_date, duration, int(row["weight"]), notes, task_list
        )
        task.save()


@when(
    'The user "{email}" attempts to edit the task list name "{list_name}" to "{new_task_list_name}'
)
def step_impl(context, email, list_name, new_task_list_name):
    find_tasklist = TaskList.objects.filter(list_name=list_name).first()
    if find_tasklist != None:
        tasklist_id = find_tasklist.id
    else:
        tasklist_id = -1
    try:
        list_str = str(new_task_list_name) if new_task_list_name is not None else ""
        context.response = context.client.put(
            reverse("edit_name", kwargs={"pk": tasklist_id}), {"list_name": list_str})
        print(context.response)
    except BaseException as e:
        context.error = e


@then('The user "{email}" shall have a task list named "{new_task_list_name}"')
def step_impl(context, email, new_task_list_name):
    task_list = TaskList.objects.filter(list_name=new_task_list_name).first()
    assert_that(str(task_list), not_none())


@then('"{new_task_list_name}" shall include "{task_name}"')
def step_impl(context, new_task_list_name, task_name):
    task = Task.objects.filter(description=task_name).first()
    assert_that(str(task.tasklist), new_task_list_name)
