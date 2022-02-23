from rest_framework.decorators import api_view
from django.http import HttpResponse
from tasklists.models import Task


def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


@api_view(["GET"])
def view_all_tasks(request):
    return Task.objects.filter(pk=request.user.id).all()

