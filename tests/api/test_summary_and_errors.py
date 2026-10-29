from django.http import JsonResponse
from django.test import RequestFactory
from rest_framework.test import APIClient

from apps.appointments.models import Appointment
from core.middleware import GlobalExceptionMiddleware, RequestLoggingMiddleware


def test_exception_middleware_hides_internal_error_details():
    request = RequestFactory().get("/api/test")
    response = GlobalExceptionMiddleware(lambda _: (_ for _ in ()).throw(RuntimeError("secret stack detail")))(request)

    assert response.status_code == 500
    assert b"secret stack detail" not in response.content
    assert b"Internal Server Error" in response.content


def test_request_logging_middleware_adds_correlation_id():
    request = RequestFactory().get("/api/test", HTTP_X_CORRELATION_ID="correlation-123")
    response = RequestLoggingMiddleware(lambda _: JsonResponse({"ok": True}))(request)

    assert response["X-Correlation-ID"] == "correlation-123"


def test_business_summary_uses_upcoming_non_cancelled_appointments(service, owner, client, future_time):
    Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.PENDING)
    Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.CANCELLED)
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.get(f"/api/businesses/{service.business_id}/summary")

    assert response.status_code == 200
    assert response.data[0]["upcoming_appointments_count"] == 1
    assert response.data[0]["expected_revenue"] == "50.00"


def test_unauthenticated_business_list_returns_401():
    response = APIClient().get("/api/businesses")

    assert response.status_code == 401
