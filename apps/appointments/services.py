from datetime import timedelta

from django.db import DatabaseError, transaction
from django.utils import timezone

from apps.businesses.models import Service

from .exceptions import AvailabilityConflict, ServiceTemporarilyLocked
from .models import Appointment


class AppointmentService:
    def __init__(self, appointment_model=Appointment, service_model=Service, now=timezone.now):
        self.appointment_model = appointment_model
        self.service_model = service_model
        self.now = now

    def create_appointment(self, client, service_id, start_time):
        with transaction.atomic():
            service = self._locked_service(service_id)
            if start_time <= self.now():
                raise ValueError("Appointments must start in the future.")
            if self._has_confirmed_conflict(service, start_time):
                raise AvailabilityConflict()
            return self.appointment_model.objects.create(
                client=client,
                service=service,
                start_time=start_time,
                status=Appointment.Status.PENDING,
            )

    def confirm_appointment(self, appointment, owner):
        with transaction.atomic():
            service = self._locked_service(appointment.service_id)
            appointment = self.appointment_model.objects.select_for_update().get(id=appointment.id)
            if service.business.owner_id != owner.id:
                raise PermissionError("You do not own this appointment.")
            if appointment.status != Appointment.Status.PENDING:
                raise ValueError("Only pending appointments can be confirmed.")
            if self._has_confirmed_conflict(service, appointment.start_time, exclude_id=appointment.id):
                raise AvailabilityConflict()
            appointment.status = Appointment.Status.CONFIRMED
            appointment.save(update_fields=["status", "updated_at"])
            self._conflicting_pending(service, appointment.start_time, appointment.id).update(
                status=Appointment.Status.CANCELLED,
                updated_at=self.now(),
            )
            return appointment

    def cancel_appointment(self, appointment, actor):
        with transaction.atomic():
            service = self._locked_service(appointment.service_id)
            appointment = self.appointment_model.objects.select_for_update().get(id=appointment.id)
            is_client = appointment.client_id == actor.id
            is_owner = service.business.owner_id == actor.id
            if not (is_client or is_owner):
                raise PermissionError("You may not cancel this appointment.")
            if is_client and appointment.start_time <= self.now():
                raise ValueError("Clients may cancel only future appointments.")
            if appointment.status == Appointment.Status.CANCELLED:
                raise ValueError("Cancelled appointments cannot be changed.")
            appointment.status = Appointment.Status.CANCELLED
            appointment.save(update_fields=["status", "updated_at"])
            return appointment

    def _locked_service(self, service_id):
        try:
            return self.service_model.objects.select_for_update(nowait=True).select_related("business").get(id=service_id)
        except DatabaseError as error:
            if getattr(error.__cause__, "pgcode", None) == "55P03":
                raise ServiceTemporarilyLocked() from error
            raise

    def _has_confirmed_conflict(self, service, start_time, exclude_id=None):
        conflicts = self._conflicting_appointments(service, start_time).filter(status=Appointment.Status.CONFIRMED)
        if exclude_id:
            conflicts = conflicts.exclude(id=exclude_id)
        return conflicts.exists()

    def _conflicting_pending(self, service, start_time, exclude_id):
        return self._conflicting_appointments(service, start_time).filter(status=Appointment.Status.PENDING).exclude(id=exclude_id)

    def _conflicting_appointments(self, service, start_time):
        duration = timedelta(minutes=service.duration_minutes)
        return self.appointment_model.objects.filter(
            service=service,
            start_time__lt=start_time + duration,
            start_time__gt=start_time - duration,
        )
