from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.appointments.models import Appointment
from apps.appointments.exceptions import ServiceTemporarilyLocked


@pytest.mark.django_db
def test_register_and_login_return_documented_contract():
    client = APIClient()
    registration = client.post("/api/auth/register", {
        "email": "CLIENT@EXAMPLE.COM",
        "password": "A-strong-password-123",
        "full_name": "New Client",
        "role": "Client",
    }, format="json")
    login = client.post("/api/auth/login", {"email": "client@example.com", "password": "A-strong-password-123"}, format="json")

    assert registration.status_code == 201
    assert registration.data["email"] == "client@example.com"
    assert login.status_code == 200
    assert login.data["token_type"] == "Bearer"
    assert login.data["expires_in"] == 3600


@pytest.mark.django_db(transaction=True)
def test_client_cannot_book_confirmed_service_window(service, client, second_client, future_time):
    appointment = Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.CONFIRMED)
    api_client = APIClient()
    api_client.force_authenticate(second_client)

    response = api_client.post("/api/appointments", {
        "service_id": str(service.id),
        "start_time": (future_time + timedelta(minutes=10)).isoformat(),
    }, format="json")

    assert appointment.status == Appointment.Status.CONFIRMED
    assert response.status_code == 409


@pytest.mark.django_db
def test_owner_sees_booking_client_details_and_client_does_not(service, owner, client, future_time):
    appointment = Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.PENDING)
    owner_api = APIClient()
    owner_api.force_authenticate(owner)
    client_api = APIClient()
    client_api.force_authenticate(client)

    owner_response = owner_api.get("/api/appointments")
    client_response = client_api.get("/api/appointments")

    assert owner_response.status_code == 200
    assert owner_response.data["results"][0]["client_email"] == client.email
    assert "client_email" not in client_response.data["results"][0]
    assert appointment.id


@pytest.mark.django_db
def test_client_cannot_read_another_owners_business_summary(service, client):
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.get(f"/api/businesses/{service.business_id}/summary")

    assert response.status_code == 403


@pytest.mark.django_db
def test_missing_business_returns_404(owner):
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.get("/api/businesses/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


@pytest.mark.django_db
def test_locked_service_returns_423(service, client, future_time, monkeypatch):
    def raise_locked(*_args, **_kwargs):
        raise ServiceTemporarilyLocked()

    monkeypatch.setattr("apps.appointments.views.AppointmentService.create_appointment", raise_locked)
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.post("/api/appointments", {
        "service_id": str(service.id),
        "start_time": future_time.isoformat(),
    }, format="json")

    assert response.status_code == 423
    assert "was not processed" in response.data["detail"]
