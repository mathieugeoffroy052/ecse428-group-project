from django.urls import path
from tasklists.views import public, private, task_list

urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("tasks/", task_list, name="task_list"),
]
