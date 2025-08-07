import time
import logging

from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog
from .utils import get_client_ip

logger = logging.getLogger("security.middleware")


class RequestTrackingMiddleware(MiddlewareMixin):
    """
    Logs each request/response loop into RequestLog.
    """

    def process_request(self, request):
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        try:
            duration = int((time.monotonic() - request._start_time) * 1000)
            RequestLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                duration_ms=duration,
                ip_address=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
            )
        except Exception as exc:
            logger.exception("Failed to log request: %s", exc)
        return response

    def process_exception(self, request, exception):
        # still log the failed request
        return self.process_response(request, getattr(request, "response", None) or exception)