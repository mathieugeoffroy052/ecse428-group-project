from django.urls import path
from tasklists.views import public, private, view_all_tasks

urlpatterns = [
    path("public/", public),
    path("private/", private),

    path("view_all_tasks/", view_all_tasks),
]
