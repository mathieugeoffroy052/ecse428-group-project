from django.urls import path
from tasklists.views import public, private

urlpatterns = [path("public/", public), path("private/", private)]
