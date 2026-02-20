from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import register_view, ProfileView, ProfileUpdateView

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
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit", ProfileUpdateView.as_view(), name="profile_edit"),
]
