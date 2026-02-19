from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_htmx.http import HttpResponseClientRedirect, retarget
from urllib.parse import urlparse

from .models import Note


class NoteBaseView(LoginRequiredMixin):
    model = Note
    fields = ("title", "content")
    success_url = reverse_lazy("notes:list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class NoteListView(NoteBaseView, ListView):
    context_object_name = "notes"


class NoteDetailView(NoteBaseView, DetailView):
    context_object_name = "note"


class NoteCreateView(NoteBaseView, CreateView):
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


class NoteUpdateView(NoteBaseView, UpdateView):
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


class NoteDeleteView(NoteBaseView, DeleteView):
    template_name = "notes/partials/_note_confirm_delete.html"
    context_object_name = "note"

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

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
