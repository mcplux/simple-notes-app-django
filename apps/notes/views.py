from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Note


@require_http_methods(["GET"])
def note_list(request: HttpRequest):
    notes = Note.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notes/note_list.html", {"notes": notes})
