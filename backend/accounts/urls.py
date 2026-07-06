from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    change_avatar,
    change_nickname,
    email_verification_view,
    login_view,
    logout_view,
    profile_settings,
    profile_view,
    register_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path("profile/", profile_view, name="profile"),
    path("settings/", profile_settings, name="settings"),
    path('change_nickname/', change_nickname, name="change_nickname"),
    path('change_avatar/', change_avatar, name="change_avatar"),
    path('verify-email/', email_verification_view, name='email_verification'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
