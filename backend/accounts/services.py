import logging
import os
import secrets

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import transaction

from .models import EmailVerificationCode

logger = logging.getLogger(__name__)

ALLOWED_EMAIL_DOMAINS = (
    "@gmail.com", "@yahoo.com", "@ukr.net", "@mail.ru",
    "@yandex.ru", "@outlook.com", "@icloud.com",
)
MAX_NICKNAME_LENGTH = 50
ALLOWED_AVATAR_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_AVATAR_SIZE = 8 * 1024 * 1024


class RegistrationError(Exception):
    pass


class VerificationError(Exception):
    pass


class ProfileError(Exception):
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


def _validate_registration(*, username: str, email: str, password: str) -> None:
    try:
        UnicodeUsernameValidator()(username)
        validate_email(email)
    except DjangoValidationError as error:
        raise RegistrationError("; ".join(error.messages)) from None

    if not email.endswith(ALLOWED_EMAIL_DOMAINS):
        raise RegistrationError(
            "Допустимые домены почты: " + ", ".join(ALLOWED_EMAIL_DOMAINS)
        )
    if User.objects.filter(username=username).exists():
        raise RegistrationError("Имя пользователя уже занято")
    if User.objects.filter(email=email).exists():
        raise RegistrationError("Email уже используется")

    try:
        validate_password(password)
    except DjangoValidationError as error:
        raise RegistrationError("; ".join(error.messages)) from None


@transaction.atomic
def register_user(*, username: str, email: str, password: str) -> User:
    _validate_registration(username=username, email=email, password=password)

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
    cleaned = nickname.strip()
    if not cleaned or len(cleaned) > MAX_NICKNAME_LENGTH:
        raise ProfileError(f"Никнейм должен быть от 1 до {MAX_NICKNAME_LENGTH} символов")

    user.profile.nickname = cleaned
    user.profile.save(update_fields=["nickname"])
    logger.debug(f"Nickname changed, user={user.username}")


def update_avatar(*, user: User, avatar) -> None:
    if avatar.size > MAX_AVATAR_SIZE:
        raise ProfileError("Файл слишком большой. Максимум 8 МБ")

    extension = os.path.splitext(avatar.name)[1].lower()
    if extension not in ALLOWED_AVATAR_EXTENSIONS:
        raise ProfileError("Допустимые форматы: JPG, PNG, GIF, WEBP")

    user.profile.avatar = avatar
    user.profile.save(update_fields=["avatar"])
    logger.debug(f"Avatar changed, user={user.username}")
