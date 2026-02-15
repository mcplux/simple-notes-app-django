from django.urls import path
from .views import note_list, note_form, note_detail

app_name = "notes"

urlpatterns = [
    path("", note_list, name="list"),
    path("tasks/create", note_form, name="create"),
    path("tasks/<int:pk>/", note_detail, name="detail"),
    path("tasks/<int:pk>/update", note_form, name="update"),
]
