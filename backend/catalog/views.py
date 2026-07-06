import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from comments import services as comment_services

from . import services
from .models import AnimeDescription

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def _anime_page(request, anime_name, template):
    anime = get_object_or_404(AnimeDescription, name=anime_name)

    services.register_view_event(
        anime=anime,
        user=request.user,
        ip_address=get_client_ip(request),
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(request.path)

        try:
            comment_services.create_comment(
                user=request.user,
                anime=anime,
                text=request.POST.get("comment", ""),
            )
        except comment_services.CommentRejected:
            pass

        return redirect(request.path)

    comments = comment_services.comments_for_anime(anime)
    paginator = Paginator(comments, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    user_rating = None
    watch_progress = None
    if request.user.is_authenticated:
        user_rating = request.user.anime_ratings.filter(anime=anime).first()
        watch_progress = request.user.watch_progress.filter(anime=anime).first()

    return render(request, template, {
        "anime": anime,
        "comments": page_obj,
        "user_rating": user_rating,
        "avg_rating": services.average_rating(anime),
        "total_views": anime.views.count(),
        "watch_progress": watch_progress,
    })


def steins_gate_page(request):
    return _anime_page(request, "Steins;Gate", "steins-gate_page.html")


def steins_gate_zero_page(request):
    return _anime_page(request, "Steins;Gate 0", "steins-gate-zero_page.html")


def steins_gate_load_region_page(request):
    return _anime_page(request, "Steins;Gate: Load Region of Deja Vu", "steins_gate_load_region_page.html")


def steins_gate_missing_link(request):
    return _anime_page(request, "Steins;Gate: Kyoukaimenjou no Missing Link", "steins_gate_missing_link.html")


def future_gadget_laboratory_page(request):
    popular_anime = AnimeDescription.objects.annotate(
        views_count=Count('views')
    ).order_by('-views_count')[:4]

    return render(request, "future_gadget_laboratory.html", {"popular_anime": popular_anime})


@login_required
def rate_anime(request, anime_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    anime = get_object_or_404(AnimeDescription, id=anime_id)

    try:
        rating_value = int(request.POST.get("rating", 0))
        avg_rating = services.rate_anime(
            user=request.user, anime=anime, rating=rating_value
        )
    except ValueError:
        return JsonResponse({"error": "Invalid rating"}, status=400)

    return JsonResponse({
        "success": True,
        "avg_rating": round(avg_rating, 1) if avg_rating else 0,
        "user_rating": rating_value,
    })
