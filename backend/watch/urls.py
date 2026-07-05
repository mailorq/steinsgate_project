from django.urls import path

from .views import save_watch_progress

urlpatterns = [
    path("anime/<int:anime_id>/progress/", save_watch_progress, name="save_watch_progress"),
]
