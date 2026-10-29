from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.businesses.models import Business, Service
from apps.users.models import DemoSeedMarker, User


class Command(BaseCommand):
    help = "Creates the deterministic BookIt development dataset once."

    def handle(self, *args, **options):
        with transaction.atomic():
            if DemoSeedMarker.objects.filter(key="demo-seed-v1").exists():
                self.stdout.write(self.style.WARNING("Demo data already exists; skipping seed."))
                return

            anchor = timezone.now().replace(second=0, microsecond=0)
            DemoSeedMarker.objects.create(key="demo-seed-v1", anchor_at=anchor)
            owners = [
                User.objects.create_user(
                    email=f"owner{index}@bookit.local",
                    password="BookItDemo123!",
                    full_name=f"Demo Owner {index}",
                    role=User.Role.BUSINESS_OWNER,
                )
                for index in range(1, 6)
            ]
            clients = [
                User.objects.create_user(
                    email=f"client{index}@bookit.local",
                    password="BookItDemo123!",
                    full_name=f"Demo Client {index}",
                    role=User.Role.CLIENT,
                )
                for index in range(1, 11)
            ]
            businesses = []
            for index in range(20):
                owner = owners[index % len(owners)]
                businesses.append(Business.objects.create(
                    owner=owner,
                    name=f"Demo Business {index + 1}",
                    category=("Barber" if index % 2 == 0 else "Physiotherapy"),
                ))
            services = []
            for index in range(50):
                business = businesses[index % len(businesses)]
                services.append(Service.objects.create(
                    business=business,
                    name=f"Service {index + 1} with Specialist {(index % 3) + 1}",
                    duration_minutes=(30 if index % 2 == 0 else 45),
                    price=Decimal("35.00") + Decimal(index),
                ))
            statuses = [Appointment.Status.PENDING, Appointment.Status.CONFIRMED, Appointment.Status.CANCELLED]
            for index in range(200):
                service = services[index % len(services)]
                client = clients[index % len(clients)]
                start_time = anchor + timedelta(days=(index % 9) - 3, hours=(index // 9) % 8)
                Appointment.objects.create(
                    service=service,
                    client=client,
                    start_time=start_time,
                    status=statuses[index % len(statuses)],
                )
            self.stdout.write(self.style.SUCCESS("Created BookIt development demo data."))
