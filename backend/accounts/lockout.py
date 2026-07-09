import logging
import time

from django.core.cache import cache

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")

# Блок ставится после SOFT_LIMIT неудач и обнуляет счётчик, так что в каждой
# серии гарантированы SOFT_LIMIT свежих попыток. Серии считаются отдельно:
# каждая (HARD_LIMIT / SOFT_LIMIT)-я серия в окне SERIES_TTL — длинный блок.
SOFT_LIMIT = 5
SOFT_BLOCK_SECONDS = 30
HARD_LIMIT = 20
HARD_BLOCK_SECONDS = 600
SERIES_TTL = 900

_HARD_EVERY = HARD_LIMIT // SOFT_LIMIT


class LockedOut(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Слишком много попыток. Повторите через {retry_after} сек")


def _fails_key(scope: str, ip: str) -> str:
    return f"lockout:{scope}:{ip}:fails"


def _series_key(scope: str, ip: str) -> str:
    return f"lockout:{scope}:{ip}:series"


def _block_key(scope: str, ip: str) -> str:
    return f"lockout:{scope}:{ip}:block"


def _increment(key: str) -> int:
    if cache.add(key, 1, timeout=SERIES_TTL):
        return 1
    return cache.incr(key)


def check_blocked(scope: str, ip: str | None) -> None:
    if not ip:
        return
    try:
        blocked_until = cache.get(_block_key(scope, ip))
    except Exception:
        logger.exception("Lockout storage unavailable, check skipped")
        return
    if blocked_until is None:
        return
    retry_after = int(blocked_until - time.time())
    if retry_after > 0:
        raise LockedOut(retry_after)


def register_failure(scope: str, ip: str | None) -> None:
    if not ip:
        return
    try:
        fails = _increment(_fails_key(scope, ip))
        if fails < SOFT_LIMIT:
            return

        cache.delete(_fails_key(scope, ip))
        series = _increment(_series_key(scope, ip))
        if series >= _HARD_EVERY:
            block_seconds = HARD_BLOCK_SECONDS
            cache.delete(_series_key(scope, ip))
        else:
            block_seconds = SOFT_BLOCK_SECONDS

        cache.set(_block_key(scope, ip), time.time() + block_seconds, timeout=block_seconds)
    except Exception:
        logger.exception("Lockout storage unavailable, failure not counted")
        return
    security_logger.warning(
        f"IP blocked, scope={scope}, ip={ip}, series={series}, duration={block_seconds}s"
    )


def reset(scope: str, ip: str | None) -> None:
    if not ip:
        return
    try:
        cache.delete(_fails_key(scope, ip))
        cache.delete(_series_key(scope, ip))
        cache.delete(_block_key(scope, ip))
    except Exception:
        logger.exception("Lockout storage unavailable, reset skipped")
