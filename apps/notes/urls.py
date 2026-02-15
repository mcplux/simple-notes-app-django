from django.urls import path
from .views import note_list, note_create

app_name = "notes"

urlpatterns = [
    path("", note_list, name="list"),
    path("tasks/new", note_create, name="create"),
]
