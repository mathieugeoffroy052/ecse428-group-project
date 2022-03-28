from django.urls import path
from tasklists.views import public, private, update_state, edit_name, task_list

urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("update-state/<int:pk>", update_state, name="update_state"),
    path("edit-name/<int:pk>", edit_name, name="edit_name"),
    path("tasks/", task_list, name="task"),
]
