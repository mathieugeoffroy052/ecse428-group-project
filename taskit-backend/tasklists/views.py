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


"""
"/api/update-state/<pk>"
    where pk = primary key (or id) of task

{
	"state": "IP"
}
"""
@api_view(["PUT"])
def update_state(request, pk):
    request = request.data
    try:
        t = Task.objects.get(pk=pk)
        s = TaskSerializer(t, data={'state': request["state"]}, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response('Exception: Data Not Found', status=status.HTTP_400_BAD_REQUEST)