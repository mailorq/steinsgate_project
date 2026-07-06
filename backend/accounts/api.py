from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from ninja import File, Router
from ninja.decorators import decorate_view
from ninja.files import UploadedFile
from ninja.security import django_auth
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

from . import services
from .schemas import LoginIn, MessageOut, NicknameIn, RegisterIn, SessionOut, UserOut, VerifyEmailIn

auth_router = Router(tags=["auth"])
profile_router = Router(tags=["profile"])


def serialize_user(user: User) -> dict:
    profile = user.profile
    return {
        "username": user.username,
        "nickname": profile.nickname or user.username,
        "email": user.email,
        "avatar_url": profile.avatar.url if profile.avatar else None,
    }


@auth_router.get("/csrf", response={204: None})
@decorate_view(ensure_csrf_cookie)
def csrf_token(request):
    return 204, None


@auth_router.get("/session", response=SessionOut)
def session(request):
    if request.user.is_authenticated:
        return {"user": serialize_user(request.user)}
    return {"user": None}


@auth_router.post(
    "/register",
    response={201: MessageOut, 400: MessageOut},
    throttle=[AnonRateThrottle(settings.API_AUTH_THROTTLE)],
)
def register(request, payload: RegisterIn):
    try:
        user = services.register_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
        )
    except services.RegistrationError as error:
        return 400, {"detail": str(error)}

    request.session["pending_user_id"] = user.id
    return 201, {"detail": "Код подтверждения отправлен на почту"}


@auth_router.post(
    "/verify-email",
    response={200: SessionOut, 400: MessageOut},
    throttle=[AnonRateThrottle(settings.API_AUTH_THROTTLE)],
)
def verify_email(request, payload: VerifyEmailIn):
    pending_user_id = request.session.get("pending_user_id")
    user = User.objects.filter(id=pending_user_id, is_active=False).first()
    if user is None:
        return 400, {"detail": "Нет ожидающей подтверждения регистрации"}

    try:
        services.verify_email(user=user, code=payload.code)
    except services.VerificationError as error:
        return 400, {"detail": str(error)}

    request.session.pop("pending_user_id", None)
    login(request, user)
    return 200, {"user": serialize_user(user)}


@auth_router.post(
    "/login",
    response={200: SessionOut, 400: MessageOut},
    throttle=[AnonRateThrottle(settings.API_AUTH_THROTTLE)],
)
def login_view(request, payload: LoginIn):
    user = services.authenticate_user(
        request=request, username=payload.username, password=payload.password
    )
    if user is None:
        return 400, {"detail": "Неверное имя пользователя или пароль"}

    login(request, user)
    return 200, {"user": serialize_user(user)}


@auth_router.post("/logout", response={204: None}, auth=django_auth)
def logout_view(request):
    logout(request)
    return 204, None


@profile_router.patch("", response={200: UserOut, 400: MessageOut}, auth=django_auth)
def update_profile(request, payload: NicknameIn):
    try:
        services.update_nickname(user=request.user, nickname=payload.nickname)
    except services.ProfileError as error:
        return 400, {"detail": str(error)}
    return 200, serialize_user(request.user)


@profile_router.post(
    "/avatar",
    response={200: UserOut, 400: MessageOut},
    auth=django_auth,
    throttle=[AuthRateThrottle(settings.API_WRITE_THROTTLE)],
)
def upload_avatar(request, avatar: File[UploadedFile]):
    try:
        services.update_avatar(user=request.user, avatar=avatar)
    except services.ProfileError as error:
        return 400, {"detail": str(error)}
    return 200, serialize_user(request.user)
