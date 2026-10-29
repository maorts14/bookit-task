from django.http import JsonResponse
from django.test import RequestFactory
from django.test.utils import override_settings
from rest_framework.test import APIClient

from apps.appointments.models import Appointment
from apps.businesses.models import Service
from core.middleware import RequestLoggingMiddleware


@override_settings(ROOT_URLCONF="tests.urls")
def test_exception_middleware_hides_internal_error_details():
    response = APIClient().get("/explode")

    assert response.status_code == 500
    assert b"secret stack detail" not in response.content
    assert b"Internal Server Error" in response.content


def test_request_logging_middleware_adds_correlation_id():
    request = RequestFactory().get("/api/test", HTTP_X_CORRELATION_ID="correlation-123")
    response = RequestLoggingMiddleware(lambda _: JsonResponse({"ok": True}))(request)

    assert response["X-Correlation-ID"] == "correlation-123"


def test_business_summary_uses_upcoming_non_cancelled_appointments(service, owner, client, future_time):
    unused_service = Service.objects.create(
        business=service.business,
        name="Unused service",
        duration_minutes=15,
        price="20.00",
    )
    Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.PENDING)
    Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.CANCELLED)
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.get(f"/api/businesses/{service.business_id}/summary")

    assert response.status_code == 200
    summary_by_service = {str(item["service_id"]): item for item in response.data}
    assert summary_by_service[str(service.id)]["upcoming_appointments_count"] == 1
    assert summary_by_service[str(service.id)]["expected_revenue"] == "50.00"
    assert summary_by_service[str(unused_service.id)]["upcoming_appointments_count"] == 0
    assert summary_by_service[str(unused_service.id)]["expected_revenue"] == "0.00"


def test_unauthenticated_business_list_returns_401():
    response = APIClient().get("/api/businesses")

    assert response.status_code == 401
