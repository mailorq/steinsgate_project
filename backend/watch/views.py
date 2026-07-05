from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from catalog.models import AnimeDescription

from . import services


@login_required
def save_watch_progress(request, anime_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    anime = get_object_or_404(AnimeDescription, id=anime_id)

    try:
        current_time = float(request.POST.get("current_time", 0))
        duration = float(request.POST.get("duration", 0))
    except ValueError:
        return JsonResponse({"error": "Invalid progress values"}, status=400)

    progress = services.save_progress(
        user=request.user, anime=anime, current_time=current_time, duration=duration
    )

    return JsonResponse({
        "success": True,
        "current_time": progress.current_time,
        "duration": progress.duration,
        "percentage": progress.progress_percentage,
    })
