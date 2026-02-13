from django.contrib.auth.views import LoginView
from django.urls import path
from .views import register_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
]
