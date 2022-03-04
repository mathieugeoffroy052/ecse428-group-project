from django.urls import path
from tasklists.views import public, private, update_state, task_list

urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("update-state/<int:pk>", update_state, name="update_state"),
    path("tasks/", task_list, name="task_list"),
]
