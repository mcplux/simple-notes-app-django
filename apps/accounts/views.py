from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import render, redirect

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
