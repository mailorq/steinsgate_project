import logging

from ninja.throttling import AnonRateThrottle, AuthRateThrottle

logger = logging.getLogger(__name__)


class FailOpenMixin:
    """недоступное хранилище счетчиков не должно ронять api"""

    def allow_request(self, request):
        try:
            return super().allow_request(request)
        except Exception:
            logger.exception("Throttle storage unavailable, request allowed")
            return True


# у каждого окна свой scope инстансы с общим scope делят счетчик в кеше,
# и второй уровень лимита считал бы те же запросы


class AnonBurstThrottle(FailOpenMixin, AnonRateThrottle):
    scope = "anon_burst"


class AnonSustainedThrottle(FailOpenMixin, AnonRateThrottle):
    scope = "anon_sustained"


class AuthBurstThrottle(FailOpenMixin, AuthRateThrottle):
    scope = "auth_burst"


class AuthSustainedThrottle(FailOpenMixin, AuthRateThrottle):
    scope = "auth_sustained"


def anon_throttles(burst_rate: str, sustained_rate: str) -> list:
    return [AnonBurstThrottle(burst_rate), AnonSustainedThrottle(sustained_rate)]


def auth_throttles(burst_rate: str, sustained_rate: str) -> list:
    return [AuthBurstThrottle(burst_rate), AuthSustainedThrottle(sustained_rate)]
