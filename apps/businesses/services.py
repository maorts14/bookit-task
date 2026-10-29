from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import Business, Service


class BusinessService:
    def __init__(self, business_model=Business, service_model=Service, now=timezone.now):
        self.business_model = business_model
        self.service_model = service_model
        self.now = now

    def create_business(self, owner, **fields):
        return self.business_model.objects.create(owner=owner, **fields)

    def create_service(self, business, **fields):
        return self.service_model.objects.create(business=business, **fields)

    def service_summary(self, business):
        upcoming = Q(appointments__start_time__gt=self.now(), appointments__status__in=["Pending", "Confirmed"])
        return self.service_model.objects.filter(business=business).annotate(
            upcoming_appointments_count=Count("appointments", filter=upcoming),
            expected_revenue=Coalesce(
                ExpressionWrapper(Count("appointments", filter=upcoming) * F("price"), output_field=DecimalField(max_digits=12, decimal_places=2)),
                Value(0),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            ),
        )
