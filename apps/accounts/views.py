from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .forms import RegisterForm

User = get_user_model()


def register_view(request: HttpRequest):
    # Redirect if user is authenticated
    if request.user.is_authenticated:
        return redirect("notes:list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("notes:list")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


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
