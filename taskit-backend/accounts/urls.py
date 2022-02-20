from django.urls import path
from accounts.views import sign_up

urlpatterns = [
    path("signup/", sign_up),
]