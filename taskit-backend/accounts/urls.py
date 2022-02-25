from django.urls import path
from accounts.views import sign_up
from accounts.views import login_request
from accounts.views import logout_request

urlpatterns = [
    path("sign_up/", sign_up),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name="logout"),
]
