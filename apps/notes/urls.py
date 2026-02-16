from django.urls import path
from .views import note_list, note_form, note_detail, note_delete

app_name = "notes"

urlpatterns = [
    path("", note_list, name="list"),
    path("notes/create", note_form, name="create"),
    path("notes/<int:pk>/", note_detail, name="detail"),
    path("notes/<int:pk>/update", note_form, name="update"),
    path("notes/<int:pk>/delete", note_delete, name="delete"),
]
