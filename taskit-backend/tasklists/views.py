from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.http import HttpResponse
from tasklists.serializers import TaskSerializer, TaskListSerializer
from tasklists.models import Task, TaskList


def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


# API to update task (state)
@api_view(["PUT"])
def update_state(request, pk):
    """
    PUT
    "/api/update-state/<pk>"
        where pk = primary key (or id) of task

    {
        "state": "IP"
    }
    """
    request = request.data
    if not request["state"]:
        return Response("Invalid task state", status=status.HTTP_400_BAD_REQUEST)
    try:
        t = Task.objects.get(pk=pk)
        s = TaskSerializer(t, data={"state": request["state"]}, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response("Exception: Data Not Found", status=status.HTTP_400_BAD_REQUEST)


# APIs for Task
@api_view(["GET", "PUT", "POST", "DELETE"])
def task(request):
    if request.method == "GET":
        return list_tasks(request)
    elif request.method == "POST":
        return post_task(request)
    elif request.method == "PUT":
        return edit_task(request)
    elif request.method == "DELETE":
        return remove_task(request)
    else:
        return Response(
            {"error": f"Invalid HTTP method {request.method}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def list_tasks(request):
    """
    GET
    """
    tasks = Task.objects.filter(owner=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_task(request):
    """
    POST:
    {
        "description": "eat chocolate",
        "due_datetime":"2022-02-26T01:34:41+00:00",
        "estimated_duration": "03:00:00",
        "weight": 10000
    }
    """
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(
            {"data": serializer.data, "success": "Task created succesfully."},
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def edit_task(request):
    """
    EDIT:
    {
        "id": 1,
        "description": "eat banana",
        "due_datetime":"2040-02-26T01:34:41+00:00",
        "estimated_duration": "09:00:00",
        "weight": 1,
        "state": "IP",
        "notes": "hmmmm delicious"
    }
    """
    task_id = request.data["id"]
    tasks = Task.objects.filter(id=task_id)
    if tasks:
        task = tasks.first()
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                {"data": serializer.data, "success": "Task updated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "This field cannot be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


def remove_task(request):
    """
    DELETE:
    {
        "id": 123
    }
    """
    task_id = request.data["id"]
    tasks = Task.objects.filter(id=task_id)
    if tasks:
        task = tasks.first()
        task.delete()
        return Response({"success": "Task deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# APIs for TaskList
@api_view(["GET", "POST", "DELETE"])
def task_list(request):
    if request.method == "POST":
        return post_task_list(request)
    elif request.method == "GET":
        return list_task_list(request)
    elif request.method == "DELETE":
        return remove_task_list(request)
    else:
        return Response(
            {"error": f"Invalid HTTP method {request.method}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def list_task_list(request):
    """
    GET
    """
    tasklists = TaskList.objects.filter(owner=request.user)
    serializer = TaskListSerializer(tasklists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_task_list(request):
    """
    POST:
    {
        "list_name":"School Work",
    }
    """
    serializer = TaskListSerializer(data=request.data)

    if serializer.is_valid():
        # Check that the user doesn't already have a task list with the given name
        new_list_name = request.data["list_name"]
        if TaskList.objects.filter(owner=request.user, list_name=new_list_name).first():
            return Response(
                {"error": "This list name already exists."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer.save(owner=request.user)
        return Response(
            {"data": serializer.data, "success": "Task list created succesfully."},
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def remove_task_list(request):
    """
    DELETE:
    {
        "id": 123
    }
    """
    if "id" not in request.data:
        return Response(
            {"error": "This field is blank."}, status=status.HTTP_400_BAD_REQUEST
        )
    id = request.data["id"]
    taskLists = TaskList.objects.filter(id=id)
    if taskLists:
        taskList = taskLists.first()
        taskList.delete()
        return Response(
            {"success": "Task list deleted successfully."}, status=status.HTTP_200_OK
        )
    else:
        return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# API for editing a task list name
@api_view(["PUT"])
def edit_name(request, pk):
    """
    PUT
    "/api/edit-name/<pk>"
        where pk = primary key (or id) of tasklist

    {
        "list_name": "grocery"
    }
    """

    try:
        t = TaskList.objects.get(pk=pk)
        s = TaskListSerializer(t, data={"list_name": request.data["list_name"]})
        if s.is_valid():
            new_list_name = request.data["list_name"]
            if TaskList.objects.filter(
                owner=request.user, list_name=new_list_name
            ).first():
                return Response(
                    {"error": "This list name already exists."},
                    status=status.HTTP_409_CONFLICT,
                )
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid list name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except TaskList.DoesNotExist:
        return Response(
            {"error": "Task List Not found"}, status=status.HTTP_400_BAD_REQUEST
        )
