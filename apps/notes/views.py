from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect, retarget

from .forms import NoteForm
from .models import Note


@require_http_methods(["GET"])
def note_list(request: HttpRequest):
    notes = Note.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notes/note_list.html", {"notes": notes})


@require_http_methods(["GET", "POST"])
def note_form(request: HttpRequest, pk=None):
    note = get_object_or_404(Note, pk=pk, user=request.user) if pk else None
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            if pk is None:
                note.user = request.user
            note.save()

            if request.htmx:
                return HttpResponseClientRedirect(reverse("notes:list"))

            return redirect("notes:list")

        elif request.htmx:
            return render(
                request,
                "notes/partials/_note_form.html",
                {"form": form, "note": note},
            )

        else:
            raise PermissionDenied()
    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "notes/note_form.html",
        {"form": form, "note": note},
    )


@require_http_methods(["GET"])
def note_detail(request: HttpRequest, pk: int):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, "notes/note_detail.html", {"note": note})


@require_http_methods(["GET", "POST"])
def note_delete(request: HttpRequest, pk: int):
    if not request.htmx:
        raise PermissionDenied()

    note = get_object_or_404(Note, pk=pk, user=request.user)
    is_detail_url = request.htmx.current_url.endswith(
        reverse("notes:detail", args=(note.pk,))
    )
    if request.method == "POST":
        note.delete()

        if is_detail_url:
            return HttpResponseClientRedirect(reverse("notes:list"))

        notes = Note.objects.filter(user=request.user).order_by("-created_at")
        response = render(
            request,
            "notes/partials/_note_list.html",
            {"notes": notes},
        )

        return retarget(response, "#note-list")

    return render(
        request,
        "notes/partials/_note_delete_confirmation.html",
        {"note": note},
    )
