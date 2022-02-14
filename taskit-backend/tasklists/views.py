from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages



def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(["GET"])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


# Login upon request
def login_request(request):
    if(request.method == "POST"):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not NONE:
                login(request, user)
                messages.info(request, f"Successfully logged in as {username}")
                return redirect("main:Home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
          

    form = AuthenticationForm()
    return render(request, "main/login.html", {"form":form})


# Logout upon request
def logout_request(request):
    logout(request)
    messages.inf(request, "Successfully logged out")
    return redirect("main:Home")