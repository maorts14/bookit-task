import logging
import time
import uuid

from django.http import JsonResponse


logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            return self.process_exception(request, None)

    def process_exception(self, request, exception):
        logger.error("Unhandled request exception", exc_info=exception)
        return JsonResponse(
            {"type": "about:blank", "title": "Internal Server Error", "status": 500},
            status=500,
            content_type="application/problem+json",
        )


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        request.correlation_id = correlation_id
        started_at = time.monotonic()
        response = self.get_response(request)
        response["X-Correlation-ID"] = correlation_id
        duration_ms = round((time.monotonic() - started_at) * 1000, 2)
        logger.info(
            "request method=%s path=%s status=%s duration_ms=%s correlation_id=%s",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            correlation_id,
        )
        return response
