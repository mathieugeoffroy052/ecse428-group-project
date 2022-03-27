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
    # request_data = {
    #     "user": email if email != None else User.objects.filter(email=email).first,
    #     "list_name": list_name if list_name != None else "",
    #     "new_task_list_name": list_name if list_name != None else "",
    # }
    find_tasklist = TaskList.objects.filter(list_name=list_name).first()
    if find_tasklist != None:
        tasklist_id = find_tasklist.id
    else:
        tasklist_id = -1
    try:
        context.response = context.client.put(
            reverse("edit_name", kwargs={"pk": tasklist_id})
        )
        print(context.response)
    except BaseException as e:
        context.error = e


@then('The user "{email}" shall have a task list named "{new_task_list_name}"')
def step_impl(context, email, new_task_list_name):
    owner = User.objects.filter(email=email)
    task_list = TaskList.objects.filter(list_name=new_task_list_name)
    assert_that(task_list, not_none)


@then('"{new_task_list_name}" shall include "{task_names}"')
def step_impl(context, new_task_list_name, task_names):
    task_list = TaskList.objects.filter(list_name=new_task_list_name)
    task = Task.objects.filter(task_names=task_names)
    assert_that(task, not_none())
