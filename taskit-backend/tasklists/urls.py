from django.urls import path
from tasklists.views import public, private, update_state

urlpatterns = [
    path("public/", public), 
    path("private/", private),
    path("update-state",  update_state)
]
