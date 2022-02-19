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
    User.objects.create_user(request["email"], request["password"])
    return Response({'success':'user created'}, status=status.HTTP_201_CREATED)


