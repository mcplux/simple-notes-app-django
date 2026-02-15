from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from .models import Note
from .forms import NoteForm


@require_http_methods(["GET"])
def note_list(request: HttpRequest):
    notes = Note.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notes/note_list.html", {"notes": notes})


@require_http_methods(["GET", "POST"])
def note_create(request: HttpRequest):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            if request.htmx:
                return HttpResponseClientRedirect(reverse("notes:list"))

            return redirect("notes:list")

        elif request.htmx:
            return render(request, "notes/partials/_note_form.html", {"form": form})

        else:
            raise PermissionDenied()
    else:
        form = NoteForm()

    return render(request, "notes/note_create.html", {"form": form})
