from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django_htmx.http import HttpResponseClientRedirect, retarget

from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    context_object_name = "notes"

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by("-created_at")


class NoteDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "note"

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ("title", "content")
    success_url = reverse_lazy("notes:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        if self.request.htmx:
            return HttpResponseClientRedirect(self.get_success_url())

        return response

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                "notes/partials/_note_form.html",
                {"form": form},
            )

        return super().form_invalid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ("title", "content")
    success_url = reverse_lazy("notes:list")

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.htmx:
            return HttpResponseClientRedirect(self.get_success_url())

        return response

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                "notes/partials/_note_form.html",
                {"form": form, "note": self.get_object()},
            )

        return super().form_invalid(form)


@login_required
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
        "notes/partials/_note_confirm_delete.html",
        {"note": note},
    )
