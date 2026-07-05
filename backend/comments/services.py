import logging
import re

import bleach
from django.db.models import Count, Q

from .models import Comment, CommentLike

logger = logging.getLogger(__name__)

URL_PATTERN = r'(https?://\S+|www\.\S+|\w+\.(com|ru|net|org|tk|xyz|bit|cc))'
MIN_LENGTH = 3
MAX_LENGTH = 2000


class CommentRejected(Exception):
    pass


def create_comment(*, user, anime, text: str) -> Comment:
    cleaned = bleach.clean(text.strip(), tags=[], strip=True)

    if re.search(URL_PATTERN, cleaned, re.IGNORECASE):
        logger.warning(f"Spam attempt blocked: {user.username} tried to post a link.")
        raise CommentRejected("Ссылки в комментариях запрещены")

    if not (MIN_LENGTH <= len(cleaned) < MAX_LENGTH):
        raise CommentRejected("Недопустимая длина комментария")

    comment = Comment.objects.create(user=user, anime=anime, text=cleaned)
    logger.info(f"Anime {anime.name} comment {cleaned} , user={user.username}")
    return comment


def comments_for_anime(anime):
    return (
        anime.comments
        .select_related("user", "user__profile")
        .annotate(
            likes=Count("comment_likes", filter=Q(comment_likes__is_like=True)),
            dislikes=Count("comment_likes", filter=Q(comment_likes__is_like=False)),
        )
    )


def toggle_reaction(*, user, comment: Comment, is_like: bool) -> dict:
    like, created = CommentLike.objects.get_or_create(
        user=user,
        comment=comment,
        defaults={"is_like": is_like},
    )

    if not created:
        if like.is_like == is_like:
            like.delete()
        else:
            like.is_like = is_like
            like.save(update_fields=["is_like"])

    counts = comment.comment_likes.aggregate(
        likes=Count("id", filter=Q(is_like=True)),
        dislikes=Count("id", filter=Q(is_like=False)),
    )
    return {
        "likes": counts["likes"],
        "dislikes": counts["dislikes"],
        "rating": counts["likes"] - counts["dislikes"],
    }
