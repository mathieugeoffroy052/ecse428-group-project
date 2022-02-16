from django.urls import path
from accounts.views import sign_up

urlpatterns = [
    path("sign_up/", sign_up),
]