from django.urls import path
import views

urlpatterns = [
    path("sign_up/", views.sign_up),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]