from django.urls import path
from accounts.views import sign_up
from knox import views as knox_views
from .views import Login

urlpatterns = [
    path("sign_up/", sign_up, name='sign_up'),
    path("login/", Login.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
]
