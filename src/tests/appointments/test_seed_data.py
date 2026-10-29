import pytest
from django.core.management import call_command

from apps.appointments.models import Appointment
from apps.businesses.models import Business, Service
from apps.users.models import User


@pytest.mark.django_db(transaction=True)
def test_seed_data_is_idempotent_and_has_required_volumes():
    call_command("seed_data")
    first_counts = (User.objects.count(), Business.objects.count(), Service.objects.count(), Appointment.objects.count())
    call_command("seed_data")

    assert first_counts == (15, 20, 50, 200)
    assert (User.objects.count(), Business.objects.count(), Service.objects.count(), Appointment.objects.count()) == first_counts
