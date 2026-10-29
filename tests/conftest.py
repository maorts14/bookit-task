from datetime import timedelta

import pytest
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.businesses.models import Business, Service
from apps.users.models import User


@pytest.fixture
def owner(db):
    return User.objects.create_user("owner@example.com", "BookItDemo123!", full_name="Owner", role=User.Role.BUSINESS_OWNER)


@pytest.fixture
def client(db):
    return User.objects.create_user("client@example.com", "BookItDemo123!", full_name="Client", role=User.Role.CLIENT)


@pytest.fixture
def second_client(db):
    return User.objects.create_user("second@example.com", "BookItDemo123!", full_name="Second Client", role=User.Role.CLIENT)


@pytest.fixture
def other_owner(db):
    return User.objects.create_user("other-owner@example.com", "BookItDemo123!", full_name="Other Owner", role=User.Role.BUSINESS_OWNER)


@pytest.fixture
def service(owner):
    business = Business.objects.create(owner=owner, name="Dana's Studio", category="Barber")
    return Service.objects.create(business=business, name="Haircut with Dana", duration_minutes=30, price="50.00")


@pytest.fixture
def other_service(other_owner):
    business = Business.objects.create(owner=other_owner, name="Other Studio", category="Physiotherapy")
    return Service.objects.create(business=business, name="Physio with Alex", duration_minutes=45, price="80.00")


@pytest.fixture
def future_time():
    return timezone.now() + timedelta(days=1)


@pytest.fixture
def pending_appointment(service, client, future_time):
    return Appointment.objects.create(service=service, client=client, start_time=future_time, status=Appointment.Status.PENDING)
