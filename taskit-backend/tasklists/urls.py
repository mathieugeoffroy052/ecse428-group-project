from django.urls import path

from tasklists.views import public, private, task_list, view_all_tasks

urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("view_all_tasks/", view_all_tasks),
    path("tasks/", task_list, name="task_list"),
]
