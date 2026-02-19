from django.urls import path
from .views import (
    note_delete,
    NoteListView,
    NoteCreateView,
    NoteUpdateView,
    NoteDetailView,
)

app_name = "notes"

urlpatterns = [
    path("", NoteListView.as_view(), name="list"),
    path("notes/create/", NoteCreateView.as_view(), name="create"),
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="detail"),
    path("notes/<int:pk>/update", NoteUpdateView.as_view(), name="update"),
    path("notes/<int:pk>/delete", note_delete, name="delete"),
]
