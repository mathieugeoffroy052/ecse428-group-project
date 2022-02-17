from django.urls import path
from accounts.views import sign_up
from . import views

urlpatterns = [
    path("sign_up/", sign_up),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]