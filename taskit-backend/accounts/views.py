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



# Login upon request
'''
{
    "username": "johnsmith",
    "password": "johnpassword"
}
'''
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