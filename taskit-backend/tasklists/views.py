from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from tasklists.serializers import TaskSerializer
from tasklists.models import Task
from datetime import datetime, timedelta, date, timezone
from django.utils.dateparse import parse_duration
import math


def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def get_urgency(request) -> (bool, float):
    request = request.data
    task = Task.objects.get(pk=request) # expecting id as integer
    task = TaskSerializer(task)
    remaining_timedelta = datetime.fromisoformat(task["due_datetime"].value) - datetime.now(timezone.utc)
    remaining_hours = remaining_timedelta.days * 24 + remaining_timedelta.seconds / (60 * 60) # hours sare the accurate depiction and most used case
    delta = parse_duration(task["estimated_duration"].value)
    estimated_hours = delta.days * 24 + delta.seconds / (60 * 60)
    late = remaining_hours < 0
    urgency = -1 * estimated_hours * remaining_hours if late else estimated_hours / remaining_hours # the later it is, the more urgent, and the sooner it is due, the more urgent
    return Response({(late, math.atan(urgency) * 2/math.pi)}, status=status.HTTP_200_OK)