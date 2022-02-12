from django.urls import path
from tasklists.views import public, private, sign_up


urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("sign_up/", sign_up),
]
