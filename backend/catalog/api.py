from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import django_auth
from ninja.throttling import AuthRateThrottle

from . import services
from .models import AnimeDescription
from .schemas import AnimeDetailOut, AnimeListOut, RatingIn, RatingOut

router = Router(tags=["catalog"])


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


@router.get("/anime", response=list[AnimeListOut])
def list_anime(request):
    return AnimeDescription.objects.all()


@router.get("/anime/{slug}", response=AnimeDetailOut)
def anime_detail(request, slug: str):
    anime = get_object_or_404(AnimeDescription, slug=slug)

    services.register_view_event(
        anime=anime,
        user=request.user,
        ip_address=get_client_ip(request),
    )

    user_rating = None
    if request.user.is_authenticated:
        rating = request.user.anime_ratings.filter(anime=anime).first()
        user_rating = rating.rating if rating else None

    return {
        "slug": anime.slug,
        "name": anime.name,
        "season": anime.appearing,
        "type": anime.type,
        "genres": anime.genres,
        "description": anime.description,
        "avg_rating": services.average_rating(anime),
        "total_views": anime.views.count(),
        "user_rating": user_rating,
    }


@router.post(
    "/anime/{slug}/rating",
    response=RatingOut,
    auth=django_auth,
    throttle=[AuthRateThrottle(settings.API_WRITE_THROTTLE)],
)
def rate_anime(request, slug: str, payload: RatingIn):
    anime = get_object_or_404(AnimeDescription, slug=slug)
    avg_rating = services.rate_anime(user=request.user, anime=anime, rating=payload.rating)

    return {
        "avg_rating": round(avg_rating, 1) if avg_rating else 0,
        "user_rating": payload.rating,
    }
