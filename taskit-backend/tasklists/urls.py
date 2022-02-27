from django.urls import path
from tasklists.views import public, private, task_list, update_state

urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("tasks/", task_list, name="task_list"),
    path("update-state/<int:pk>",  update_state)
]
