from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django_htmx.http import HttpResponseClientRedirect, retarget
from urllib.parse import urlparse

from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    context_object_name = "notes"

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


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


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "notes/partials/_note_confirm_delete.html"
    context_object_name = "note"
    success_url = reverse_lazy("notes:list")

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.pk

        self.object.delete()

        current_path = urlparse(request.htmx.current_url).path
        detail_url = reverse("notes:detail", args=(pk,))

        if current_path == detail_url:
            return HttpResponseClientRedirect(self.get_success_url())

        notes = self.get_queryset()
        response = render(
            request,
            "notes/partials/_note_list.html",
            {"notes": notes},
        )

        return retarget(response, "#note-list")
