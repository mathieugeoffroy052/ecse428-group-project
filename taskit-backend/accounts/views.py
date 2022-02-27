
from rest_framework.decorators import api_view
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login

"""
{
    "email": "john@email.com",
	"password": "johnpassword"
}
"""
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    request = request.data
    if "email" not in request or request["email"].strip():
        return Response(
            {"No email address entered."}, status=status.HTTP_400_BAD_REQUEST
        )
    if "password" not in request or request["password"].strip():
        return Response({"No password entered."}, status=status.HTTP_400_BAD_REQUEST)
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
        "token": "262bc7d283f698efdddd8d33dcea918dcb6ce05d1a4db7e052010b444083fb98"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(Login, self).post(request, format=None)
