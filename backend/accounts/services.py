import logging
import secrets

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction

from .models import EmailVerificationCode

logger = logging.getLogger(__name__)


class VerificationError(Exception):
    pass


def _generate_code() -> str:
    return f"{secrets.randbelow(10 ** 6):06d}"


def _send_code_email(email: str, code: str) -> None:
    send_mail(
        subject="Verification Email",
        message=f"Your verification code is: {code}",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[email],
        fail_silently=False,
    )


@transaction.atomic
def register_user(*, username: str, email: str, password: str) -> User:
    user = User.objects.create_user(
        username=username, email=email, password=password, is_active=False
    )
    code = _generate_code()
    EmailVerificationCode.objects.create(user=user, code=code)
    _send_code_email(email, code)
    logger.info("Verification email sent", extra={"user_email": email})
    return user


def verify_email(*, user: User, code: str) -> User:
    try:
        record = user.verification_code
    except EmailVerificationCode.DoesNotExist:
        raise VerificationError("Код не найден. Пройдите регистрацию заново.") from None

    if record.is_expired:
        raise VerificationError("Код истек. Пройдите регистрацию заново.")

    if record.attempts >= EmailVerificationCode.MAX_ATTEMPTS:
        raise VerificationError("Попытки исчерпаны. Пройдите регистрацию заново.")

    record.attempts += 1
    record.save(update_fields=["attempts"])

    if not secrets.compare_digest(record.code, code):
        remaining = EmailVerificationCode.MAX_ATTEMPTS - record.attempts
        raise VerificationError(f"Неверный код. Осталось попыток: {remaining}")

    user.is_active = True
    user.save(update_fields=["is_active"])
    record.delete()
    return user


def authenticate_user(*, request, username: str, password: str) -> User | None:
    return authenticate(request, username=username, password=password)


def update_nickname(*, user: User, nickname: str) -> None:
    user.profile.nickname = nickname
    user.profile.save(update_fields=["nickname"])
    logger.debug(f"Nickname changed, user={user.username}")


def update_avatar(*, user: User, avatar) -> None:
    user.profile.avatar = avatar
    user.profile.save(update_fields=["avatar"])
    logger.debug(f"Avatar changed, user={user.username}")
