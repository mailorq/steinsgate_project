from django.urls import path

from .views import toggle_comment_like

urlpatterns = [
    path("comment/<int:comment_id>/like/", toggle_comment_like, name="toggle_comment_like"),
]
