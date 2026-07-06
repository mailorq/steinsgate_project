from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from . import services
from .models import Comment


@login_required
def toggle_comment_like(request, comment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    comment = get_object_or_404(Comment, id=comment_id)
    is_like = request.POST.get("is_like") == "true"

    result = services.toggle_reaction(
        user=request.user, comment=comment, is_like=is_like
    )
    return JsonResponse(result)
