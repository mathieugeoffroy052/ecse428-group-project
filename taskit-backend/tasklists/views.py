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
@api_view(["GET", "POST", "DELETE"])
def task_list(request):
    if request.method == "GET":
        return list_tasks(request)
    elif request.method == "POST":
        return post_task(request)
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
        # return Response( serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"data": serializer.data, "success": "Task created succesfully."},
            status=status.HTTP_201_CREATED,
        )
    else:

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def remove_task(request):
    """
    DELETE:
    {
        "id": 123
    }
    """
    id = request.data["id"]
    tasks = Task.objects.filter(id=id)
    if tasks:
        task = tasks.first()
        task.delete()
        return Response({"success": "Task deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# APIs for TaskList
@api_view(["GET", "POST", "DELETE"])
def task_list_list(request):
    if request.method == "POST":
        return post_task_list(request)
    elif request.method == "DELETE":
        return remove_task_list(request)
    else:
        return Response(
            {"error": f"Invalid HTTP method {request.method}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def post_task_list(request):
    """
    POST:
    {
        "list_name":"School Work",
    }
    """
    serializer = TaskListSerializer(data=request.data)

    if serializer.is_valid():
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
    id = request.data["id"]
    taskLists = TaskList.objects.filter(id=id)
    if taskLists:
        taskList = taskList.first()
        taskList.delete()
        return Response({"success": "Task list deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
