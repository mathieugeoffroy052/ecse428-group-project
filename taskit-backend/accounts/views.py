# from types import NoneType
from rest_framework.decorators import api_view
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

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



# Login upon request
'''
{
    "email": "john@smith.com",
    "password": "johnpassword"
}
'''
def login_request(request):
    if(request.method == "POST"):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not NoneType:
                login(request, user)
                messages.info(request, f"Successfully logged in as {email}")
                return redirect("main:Home")
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
          

    form = AuthenticationForm()
    return render(request, "main/login.html", {"form":form})


# Logout upon request
def logout_request(request):
    logout(request)
    messages.inf(request, "Successfully logged out")
    return redirect("main:Home")
