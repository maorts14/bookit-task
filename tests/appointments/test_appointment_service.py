from datetime import timedelta

import pytest

from apps.appointments.exceptions import AvailabilityConflict
from apps.appointments.models import Appointment
from apps.appointments.services import AppointmentService


@pytest.mark.django_db(transaction=True)
def test_confirming_appointment_cancels_conflicting_pending_request(service, client, second_client, future_time):
    service_layer = AppointmentService()
    accepted = service_layer.create_appointment(client, service.id, future_time)
    competing = service_layer.create_appointment(second_client, service.id, future_time + timedelta(minutes=15))

    service_layer.confirm_appointment(accepted, service.business.owner)

    accepted.refresh_from_db()
    competing.refresh_from_db()
    assert accepted.status == Appointment.Status.CONFIRMED
    assert competing.status == Appointment.Status.CANCELLED


@pytest.mark.django_db(transaction=True)
def test_confirmed_appointment_blocks_new_overlapping_request(service, client, second_client, future_time):
    service_layer = AppointmentService()
    appointment = service_layer.create_appointment(client, service.id, future_time)
    service_layer.confirm_appointment(appointment, service.business.owner)

    with pytest.raises(AvailabilityConflict):
        service_layer.create_appointment(second_client, service.id, future_time + timedelta(minutes=10))


@pytest.mark.django_db(transaction=True)
def test_cancelling_confirmed_appointment_releases_capacity(service, client, second_client, future_time):
    service_layer = AppointmentService()
    appointment = service_layer.create_appointment(client, service.id, future_time)
    service_layer.confirm_appointment(appointment, service.business.owner)
    service_layer.cancel_appointment(appointment, client)

    replacement = service_layer.create_appointment(second_client, service.id, future_time)
    assert replacement.status == Appointment.Status.PENDING


@pytest.mark.django_db(transaction=True)
def test_back_to_back_appointment_does_not_overlap(service, client, second_client, future_time):
    service_layer = AppointmentService()
    appointment = service_layer.create_appointment(client, service.id, future_time)
    service_layer.confirm_appointment(appointment, service.business.owner)

    back_to_back = service_layer.create_appointment(
        second_client,
        service.id,
        future_time + timedelta(minutes=service.duration_minutes),
    )

    assert back_to_back.status == Appointment.Status.PENDING
