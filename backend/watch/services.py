from .models import WatchProgress


def save_progress(*, user, anime, current_time: float, duration: float) -> WatchProgress:
    progress, _ = WatchProgress.objects.update_or_create(
        user=user,
        anime=anime,
        defaults={"current_time": current_time, "duration": duration},
    )
    return progress
