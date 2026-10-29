from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.appointments.models import Appointment


@pytest.mark.django_db
def test_client_only_sees_own_appointments_and_applies_filters(service, client, second_client, future_time):
    own_confirmed = Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.CONFIRMED)
    Appointment.objects.create(service=service, client=client, start_time=future_time + timedelta(days=2), status=Appointment.Status.PENDING)
    Appointment.objects.create(service=service, client=second_client, start_time=future_time, status=Appointment.Status.CONFIRMED)
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.get("/api/appointments", {
        "from": future_time.isoformat(),
        "to": (future_time + timedelta(days=1)).isoformat(),
        "status": "Confirmed",
    })

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == str(own_confirmed.id)


@pytest.mark.django_db
def test_appointment_list_rejects_invalid_date_range(client):
    api_client = APIClient()
    api_client.force_authenticate(client)
    now = timezone.now()

    response = api_client.get("/api/appointments", {"from": now.isoformat(), "to": (now - timedelta(hours=1)).isoformat()})

    assert response.status_code == 400
    assert "to" in response.data


@pytest.mark.django_db
def test_owner_only_sees_appointments_for_owned_services(service, other_service, owner, client, second_client, future_time):
    owned_appointment = Appointment.objects.create(service=service, client=client, start_time=future_time)
    Appointment.objects.create(service=other_service, client=second_client, start_time=future_time)
    api_client = APIClient()
    api_client.force_authenticate(owner)

    response = api_client.get("/api/appointments")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == str(owned_appointment.id)


@pytest.mark.django_db
def test_appointment_create_rejects_past_time_and_business_owner(service, owner, client):
    client_api = APIClient()
    client_api.force_authenticate(client)
    owner_api = APIClient()
    owner_api.force_authenticate(owner)

    past_response = client_api.post("/api/appointments", {
        "service_id": str(service.id),
        "start_time": (timezone.now() - timedelta(minutes=1)).isoformat(),
    }, format="json")
    owner_response = owner_api.post("/api/appointments", {
        "service_id": str(service.id),
        "start_time": (timezone.now() + timedelta(days=1)).isoformat(),
    }, format="json")

    assert past_response.status_code == 400
    assert "start_time" in past_response.data
    assert owner_response.status_code == 403


@pytest.mark.django_db(transaction=True)
def test_status_transitions_enforce_actor_and_terminal_rules(service, owner, client, second_client, future_time):
    appointment = Appointment.objects.create(service=service, client=client, start_time=future_time)
    client_api = APIClient()
    client_api.force_authenticate(client)
    owner_api = APIClient()
    owner_api.force_authenticate(owner)
    outsider_api = APIClient()
    outsider_api.force_authenticate(second_client)

    client_confirm_response = client_api.patch(f"/api/appointments/{appointment.id}/status", {"status": "Confirmed"}, format="json")
    owner_confirm_response = owner_api.patch(f"/api/appointments/{appointment.id}/status", {"status": "Confirmed"}, format="json")
    outsider_cancel_response = outsider_api.patch(f"/api/appointments/{appointment.id}/status", {"status": "Cancelled"}, format="json")
    client_cancel_response = client_api.patch(f"/api/appointments/{appointment.id}/status", {"status": "Cancelled"}, format="json")
    repeated_cancel_response = client_api.patch(f"/api/appointments/{appointment.id}/status", {"status": "Cancelled"}, format="json")

    assert client_confirm_response.status_code == 403
    assert owner_confirm_response.status_code == 200
    assert outsider_cancel_response.status_code == 403
    assert client_cancel_response.status_code == 200
    assert repeated_cancel_response.status_code == 400


@pytest.mark.django_db
def test_client_cannot_cancel_past_appointment(service, client):
    appointment = Appointment.objects.create(
        service=service,
        client=client,
        start_time=timezone.now() - timedelta(days=1),
        status=Appointment.Status.CONFIRMED,
    )
    api_client = APIClient()
    api_client.force_authenticate(client)

    response = api_client.patch(f"/api/appointments/{appointment.id}/status", {"status": "Cancelled"}, format="json")

    assert response.status_code == 400
    assert "status" in response.data
