from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
from types import SimpleNamespace

def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


'''
{
	"username": "john1",
	"email": "john@email.com",
	"password": "johnpassword"
}
'''
@api_view(["POST"])
def sign_up(request):
    parsed_request = request.data
    user = User.objects.create_user(parsed_request["username"], parsed_request["email"], parsed_request["password"])
    user.save()
    return HttpResponse(
        "username: " + user.username + "<br>"+
        "email: " + user.email + "<br>" +
        "password: " + user.password + "<br>"
    )
