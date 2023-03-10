from rest_framework.decorators import api_view
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
import re


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    """
    {
        "email": "john@email.com",
        "password": "johnpassword"
    }
    """
    request = request.data
    print(f"Request data (in view): {request}")
    # Missing email
    if "email" not in request or not request["email"].strip():
        return Response(
            {"No email address entered."}, status=status.HTTP_400_BAD_REQUEST
        )
    # Invalid email
    email_validator_regex = re.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-z]{2,}$")
    if not email_validator_regex.match(request["email"]):
        return Response({"Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
    # Missing password
    if "password" not in request or not request["password"].strip():
        return Response({"No password entered."}, status=status.HTTP_400_BAD_REQUEST)
    # Email already in use
    if User.objects.filter(email=request["email"]):
        return Response(
            {"This email address is already in use."}, status=status.HTTP_409_CONFLICT
        )
    User.objects.create_user(request["email"], request["password"])
    return Response({"user created"}, status=status.HTTP_201_CREATED)


# Login
class Login(KnoxLoginView):
    """
    Request: {
        "username": "johnsmith@email.com",
        "password": "password123"
    }

    Response: {
        "expiry": "2022-02-27T04:14:53.984918-05:00",
        "token": "262bc7d283f698efdddd8d33dcea918dcb6ce05d1a4db7e052010b444083fb98",
        "has_seen_tutorial": false
    }
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        if not request.data["password"] or not request.data["password"].strip():
            return Response(
                {"No password entered."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data["username"] or not request.data["username"].strip():
            return Response(
                {"No username entered."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"Incorrect email address or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data["user"]
        login(request, user)
        return super(Login, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        # Sets has_seen_tutorial to true on the first login
        has_seen_tutorial = request.user.has_seen_tutorial
        if not has_seen_tutorial:
            request.user.has_seen_tutorial = True
            request.user.save()
        # Relevant documentation: https://james1345.github.io/django-rest-knox/views/#loginview
        return {
            "expiry": self.format_expiry_datetime(instance.expiry),
            "token": token,
            "has_seen_tutorial": has_seen_tutorial,
        }
