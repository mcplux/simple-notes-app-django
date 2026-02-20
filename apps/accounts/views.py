from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import RegisterForm


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
