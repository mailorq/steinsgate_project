from django.conf import settings
from django.db import models

from catalog.models import AnimeDescription


class WatchProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watch_progress"
    )
    anime = models.ForeignKey(
        AnimeDescription, on_delete=models.CASCADE, related_name="watch_progress"
    )
    current_time = models.FloatField(default=0)
    duration = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "anime"], name="unique_user_anime_progress"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.anime.name} - {self.current_time}s"

    @property
    def progress_percentage(self):
        if self.duration > 0:
            return (self.current_time / self.duration) * 100
        return 0
