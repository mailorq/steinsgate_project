import logging
from datetime import timedelta

from django.core.cache import cache
from django.db.models import Avg
from django.utils import timezone

from .models import AnimeDescription, AnimeRating, ViewHistory

logger = logging.getLogger(__name__)

ANIME_LIST_TTL = 300

VIEW_DEDUP_WINDOW = timedelta(hours=24)

# Средний рейтинг инвалидируется точечно при новой оценке; счётчик просмотров
# живёт по TTL — отставание на минуту для витрины безразлично
AVG_RATING_TTL = 3600
VIEWS_COUNT_TTL = 60


def _avg_rating_key(anime) -> str:
    return f"anime:{anime.id}:avg_rating"


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
    _safe_cache(cache.delete, _avg_rating_key(anime))
    return average_rating(anime)


def average_rating(anime) -> float | None:
    key = _avg_rating_key(anime)
    cached = _safe_cache(cache.get, key)
    if cached is not None:
        return cached if cached != "none" else None

    value = anime.ratings.aggregate(Avg("rating"))["rating__avg"]
    _safe_cache(cache.set, key, value if value is not None else "none", AVG_RATING_TTL)
    return value


def anime_list() -> list[dict]:
    key = "catalog:anime_list"
    cached = _safe_cache(cache.get, key)
    if cached is not None:
        return cached

    value = list(AnimeDescription.objects.values("slug", "name"))
    _safe_cache(cache.set, key, value, ANIME_LIST_TTL)
    return value


def total_views(anime) -> int:
    key = f"anime:{anime.id}:views"
    cached = _safe_cache(cache.get, key)
    if cached is not None:
        return cached

    value = anime.views.count()
    _safe_cache(cache.set, key, value, VIEWS_COUNT_TTL)
    return value


def _safe_cache(operation, *args):
    try:
        return operation(*args)
    except Exception:
        logger.exception("Cache unavailable, falling back to database")
        return None
