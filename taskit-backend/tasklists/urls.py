from django.urls import path
from tasklists.views import public, private, update_late_flag, update_state

urlpatterns = [
    path("public/", public), 
    path("private/", private),
    path("update-late", update_late_flag),
    path("update-state",  update_state)
]
