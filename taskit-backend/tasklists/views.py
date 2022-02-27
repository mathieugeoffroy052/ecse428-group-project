from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from tasklists.serializers import TaskSerializer
from tasklists.models import Task



def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


@api_view(["GET", "POST", "DELETE"])
def task_list(request):
    if request.method == "GET":
        return list_tasks(request)
    elif request.method == "POST":
        return post_task(request)
    elif request.method == "DELETE":
        return remove_task(request)
    else:
        return Response({"error": f"Invalid HTTP method {request.method}"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
