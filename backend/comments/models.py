from django.conf import settings
from django.db import models

from catalog.models import AnimeDescription


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="anime_comments"
    )
    anime = models.ForeignKey(
        AnimeDescription, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.anime.name}"

    @property
    def likes_count(self):
        return self.comment_likes.filter(is_like=True).count()

    @property
    def dislikes_count(self):
        return self.comment_likes.filter(is_like=False).count()

    @property
    def rating(self):
        return self.likes_count - self.dislikes_count


class CommentLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_likes"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_likes"
    )
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_user_comment_like"),
        ]

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.is_like else 'Dislike'} - {self.comment.id}"
