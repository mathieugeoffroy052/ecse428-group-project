from rest_framework.decorators import api_view
from django.http import HttpResponse
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

'''
{
	"email": "john@email.com",
	"password": "johnpassword"
}
'''
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    request = request.data
    try:
        if "password" not in request: 
            return Response({'No password entered.'},  status=status.HTTP_401_UNAUTHORIZED)
        if "email" not in request:
            return Response({'No email address entered.'},  status=status.HTTP_401_UNAUTHORIZED)
        User.objects.create_user(request["email"], request["password"])
        return Response({'user created'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        if str(e) == "UNIQUE constraint failed: accounts_user.email":
            return Response({'This email address is already in use.'}, status=status.HTTP_401_UNAUTHORIZED)
