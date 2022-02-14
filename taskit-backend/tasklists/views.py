from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")

