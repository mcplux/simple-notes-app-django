from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView

from .forms import RegisterForm

User = get_user_model()


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")
    success_message = "User created successfully"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ("first_name", "last_name", "email")
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")
    success_message = "Profile updated successfully"

    def get_object(self):
        return self.request.user


class ProfilePasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "accounts/profile_change-password.html"
    success_url = reverse_lazy("profile")
    success_message = "Password changed successfully"
