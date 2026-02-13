from django.urls import path
from .views import note_list

app_name = "notes"

urlpatterns = [
    path("", note_list, name="list"),
]
