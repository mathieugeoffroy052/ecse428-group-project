from django.urls import path
from tasklists.views import public, private, task_list, get_urgency

urlpatterns = [
    path("public/", public),
    path("private/", private),
    path("tasks/", task_list),
    path("get_urgency/", get_urgency),
]
