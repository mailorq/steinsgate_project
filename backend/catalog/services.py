from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone

from .models import AnimeRating, ViewHistory

VIEW_DEDUP_WINDOW = timedelta(hours=24)


def register_view_event(*, anime, user, ip_address):
    viewer = user if user is not None and user.is_authenticated else None
    since = timezone.now() - VIEW_DEDUP_WINDOW

    recent = ViewHistory.objects.filter(anime=anime, viewed_at__gte=since)
    if viewer is not None:
        recent = recent.filter(user=viewer)
    else:
        recent = recent.filter(user__isnull=True, ip_address=ip_address)

    if recent.exists():
        return None

    return ViewHistory.objects.create(anime=anime, user=viewer, ip_address=ip_address)


def rate_anime(*, user, anime, rating: int) -> float | None:
    if not 1 <= rating <= 5:
        raise ValueError("Оценка должна быть от 1 до 5")

    AnimeRating.objects.update_or_create(
        user=user, anime=anime, defaults={"rating": rating}
    )
    return average_rating(anime)


def average_rating(anime) -> float | None:
    return anime.ratings.aggregate(Avg("rating"))["rating__avg"]
